# -*- coding: utf-8 -*-
##############################################################################
# Adaptation to export product fitments to Vehicle Fits in magento shop.
# Sinergiainformatica.net
# Author : David Hernandez. 2015
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from osv import fields, osv
import psycopg2
import csv
import paramiko
import openerp.tools as tools
import base64
import os
from StringIO import StringIO


class vehicle_config(osv.osv):
    def import_file(self, cr, uid, ids, context=None):
        fileobj = TemporaryFile('w+')
        fileobj.write(base64.decodestring(data))
        return

    def test_sftp_connection(self, cr, uid, ids, context=None):
        for sftp_server in self.browse(cr, uid, ids, context=context):
            transport = False
            server = sftp_server.sftp_host
            port = sftp_server.sftp_port

        try:
            transport = paramiko.Transport((server, port))
            private_key = StringIO(base64.standard_b64decode(sftp_server.sftp_pem))
            if private_key:
                mykey = paramiko.RSAKey.from_private_key(private_key)
                username = sftp_server.sftp_user
                transport.connect(username=username, pkey=mykey)

        except Exception, e:
            raise osv.except_osv("Connection Test Failed!",
                                 "Here is what we got instead:\n %s" % tools.ustr(e))
        finally:
            try:
                if transport: transport.close()
            except Exception:
                # ignored, just a consequence of the previous exception
                pass
        raise osv.except_osv("Connection Test Succeeded!", "Everything seems properly set up!")

    _name = 'vehicle.config'
    _description = 'Configuration for Vehicle Fits ftp link'
    _table = 'vehiclefits_config'
    _columns = {

        'name': fields.char('Name', size=20),
        'vf_url': fields.char('Url', size=30, help="Url to Magento Web"),
        'sftp_user': fields.char('Ftp user', size=20, required=True),
        'sftp_password': fields.char('Ftp password', size=20, required=False),
        'sftp_pem': fields.binary('RSA Key', required=True),
        'sftp_host': fields.char('FTP IP host', size=15, required=True),
        'sftp_port': fields.integer('Ftp Port', help='Port of the connection'),
        'sftp_local_file': fields.char('Full path to local csv file'),
        'sftp_remote_file': fields.char('Name of remote file', help="Default name for import is"
                                                                    " product-fitments-import.csv"),
        'sftp_remote_dir': fields.char('Full remote path'),
        'erp_host': fields.char('Erp host', size=20, required=True),
        'erp_user': fields.char('Erp DB user', size=15, required=True),
        'erp_password': fields.char('Erp password', size=20, required=True),
        'erp_db': fields.char('Erp DB', size=20, required=True)

    }


vehicle_config()


class VehicleExport(osv.osv):
    def export_to_magento(self, cr, uid, ids, context=None):
        conf_obj = self.pool.get('vehicle.config')
        conf_ids = conf_obj.search(cr, uid, [('id', '=', 1)])
        for sftp_server in conf_obj.browse(cr, uid, conf_ids):
            host = sftp_server.erp_host
            dbname = sftp_server.erp_db
            user = sftp_server.erp_user
            password = sftp_server.erp_password
            connection_parameters = "host=%s dbname=%s user=%s password=%s" % (host, dbname, user, password)

        for date in self.browse(cr, uid, ids):
            dat_from = date.date_from
            dat_to = date.date_to

        # Define our connection string
        conn_string = connection_parameters
        # get a connection, if a connect cannot be made an exception will be raised here
        conn = psycopg2.connect(conn_string)
        # conn.cursor will return a cursor object, you can use this cursor to perform queries
        cursor = conn.cursor()

        # query
        cursor.execute(" SELECT default_code AS sku,CASE "
                       " WHEN type='MXSC'  THEN 'Maxiscooter'"
                       " WHEN type='MARCH' THEN 'Marchas 50-80cc' "
                       " WHEN type='MARCH2' THEN 'Marchas 125cc' "
                       " WHEN type='SCOOT' THEN 'Scooters 50cc'"
                       " WHEN type='SCOOT2' THEN 'Scooter 100-600cc'"
                       " WHEN type='PBKE' THEN 'Pitbike 4T'"
                       " WHEN type='PBIKE' THEN 'PocketBike'"
                       " WHEN type='VESP' THEN 'Vespas Clasicas 50-200cc'"
                       " END As make, brand AS model, model AS year FROM scooter_asociaciones"
                       " LEFT JOIN scooter_model ON"
                       " scooter_asociaciones.model_id = scooter_model.id"
                       " LEFT JOIN marcas_scooter ON"
                       " scooter_asociaciones.brand_id = marcas_scooter.id"
                       " LEFT JOIN scooter_compat_with_product_rel ON"
                       " scooter_asociaciones.id = scooter_compat_with_product_rel.scooter_id"
                       " LEFT JOIN product_product ON"
                       " product_product.id = scooter_compat_with_product_rel.product_id"
                       " WHERE scooter_asociaciones.write_date BETWEEN '%s' AND '%s'" % (dat_from, dat_to),
                       " ORDER BY make ")

        records = ()
        records = cursor.fetchall()

        with open('/opt/fitments/models-to-update.csv', 'w') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(('sku', 'make', 'model', 'year'))
            for row in records:
                writer.writerow([unicode(s).encode("utf-8") for s in row])
            conn.close()

        conf_line_obj = self.pool.get('vehicle.config')
        conf_line_ids = conf_line_obj.search(cr, uid, [('id', '=', 1)])
        for x in conf_line_obj.browse(cr, uid, conf_line_ids):
                pem = x.sftp_pem
                host = x.sftp_host
                user = x.sftp_user
                port = x.sftp_port
                rdir = x.sftp_remote_dir
                rfile = x.sftp_remote_file
                lfile = x.sftp_local_file

        # Create the transport with paramiko
        key = StringIO(base64.standard_b64decode(pem))
        mykey = paramiko.RSAKey.from_private_key(key)

        transport = paramiko.Transport((host, port))
        transport.connect(username=user, pkey=mykey)
        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.chdir(rdir)
        remotepath = rdir + '/' + rfile
        localpath = lfile

        # Push Csv
        sftp.put(localpath, remotepath)
        sftp.close()
        transport.close()

    _name = 'vehicle.export'
    _description = 'Wizard to export fitments to Vehicle fits'

    _columns = {
        'date_from': fields.datetime('Date From'),
        'date_to': fields.datetime('Date To')

    }


VehicleExport()