import pymysql
import re
import time
import six

__version__ = "$Revision: 21 $"  # version number for this library

"""========================================================================
Changes made:
21: TT(03/12/14),  Added convert_Dict_fromOStoAR(), convert_Bytes().
20: TT(01/25/14),  Added update_results and Fixed get_results.
19: TM(12/16/13),  Fixed escaping single quote and backlash in insert_results.
18: TM(12/12/13),  Raised Exception for insert_results and delete_results.
                   Fixed some print statements.
17: TM(12/11/13),  PEP8 and DOC string Compliance plus tracking version.
"""


class AUTORESULT():
    """
    Python library for inserting data into WildPacket's AutoResult database
    """
    def __init__(self, notice='autoresult'):
        self.notice = notice

    def connect_db(self):
        """
        Connect to database with given parameters
            if error, returns msg.
        """
        try:
            self.cursor = pymysql.connect(host='10.4.100.4', port=3306,
                                          user='root', passwd='wildpackets',
                                          db='test').cursor()
            print('done')
        except Exception:
            print("Error(%s): Can't connect to database" % (self.notice))

    def count_results(self, auto_dict={}):
        """
        Count number of results matching given dictionary.
             if successful, return string with count number.
             if error, return msg.
        """
        mySQL_string = 'select * from result'
        if len(auto_dict) != 0:
            mySQL_string += ' where '
            counter = 0
            for key, value in auto_dict.iteritems():
                counter += 1
                if (key != 'DATE'):
                    # TODO: verify this replacement works as desired under Python 3.
                    v = str(value).replace('\\', '\\\\')
                    mySQL_string += f'{key} = \'{v}\''
                    if counter != len(auto_dict):
                        mySQL_string += ' AND '
        try:
            count = self.cursor.execute(mySQL_string)
            return f'Info({self.notice}): {count} entry(s) is found'
        except Exception:
            print(f'Error({self.notice}): Can\'t find result from database, '
                  f'please review the following mySQL_string: {mySQL_string}')
            for key in auto_dict.keys():
                if (0 == self.cursor.execute(
                        'SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '
                        '"result" and COLUMN_NAME = f"{key}"')):
                    print(f'Error({self.notice}): Can\'t find result from database, \'{key}\' is '
                          f'not a COLUMN_NAME.')

    def delete_results(self, auto_dict, user_prompt=0):
        """
        Delete results from database with matching spec from given
        dictionary. if dictionary is empty, delete is skipped.
            -user_prompt=1: prompt if user want to delete
            if user_prompt is not 1 or 0, then check 1st character for y or n.
            if user_prompt is specified, user_prompt default to 0.
        """
        if len(auto_dict) == 0:
            print(f'Error({self.notice}): Given dictionary is empty, skipping delete result')
            return
        mySQL_del_string = 'delete from result where '
        counter = 0
        for key, value in auto_dict.iteritems():
            counter += 1
            if (key != 'DATE'):
                mySQL_del_string += f'{key} = \'str(value).replace("\\", "\\\\")\''
                if (counter != len(auto_dict)):
                    mySQL_del_string += ' AND '
        if user_prompt != 0 and user_prompt != 1:
            user_prompt = 1 if user_prompt[0].lower() == 'y' else 0
        try:
            # prompt if user wants to delete result or not.
            msg = f'Info({self.notice}): Delete result from autoresult [0 or 1]?:'
            user_input = not user_prompt or int(six.input(msg))
            if user_input == 1:
                del_count = self.cursor.execute(mySQL_del_string)
                return f'Info({self.notice}): {del_count} entry(s) is deleted'
            else:
                print(f'Info({self.notice}): Skipped deleting result from autoresult')
        except Exception:
            msg = f'Can\'t delete result from database, mySQL_del_string: {mySQL_del_string}'
            print(f'Error({self.notice}): {msg}')
            for key in auto_dict.keys():
                if 0 == self.cursor.execute(
                        'SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '
                        f'"result" and COLUMN_NAME = "{key}"'):
                    print(f'Error({self.notice}): Can\'t delete result from database, '
                          f'\'{key}\' is not a COLUMN_NAME.')
            raise Exception(msg)

    def get_latest_counter(self):
        """
        Get the row_id of latest entry in database.
            if successful, return integer of row_id.
            if error, return msg.
        """
        mySQL_string = 'select MAX(COUNTER) from result'
        try:
            self.cursor.execute(mySQL_string)
            counter = self.cursor.fetchone()[0]
            return int(counter)
        except Exception:
            print(f'Error({self.notice}): Can\'t get the latest counter id '
                  f'with mySQL_string: {mySQL_string}')

    def get_list_of_ranges(self, start, end, auto_dict={}):
        """
        Get a list of row id which matches given dictionary between given start
        and end row id.
            if successful, return a list of row ids.
            if error, return msg.
        """
        mySQL_string = f'select COUNTER from result where COUNTER >= {start} and COUNTER <= {end}'
        if len(auto_dict) != 0:
            for key, value in auto_dict.iteritems():
                mySQL_string += ' and %s = \'%s\'' % (str(key), str(value))
        try:
            self.cursor.execute(mySQL_string)
            count = [str(i[0]) for i in self.cursor.fetchall()]
            return sorted(count)
        except Exception:
            print(f'Error({self.notice}): Can\'t get the list of ranges for mySQL_string: '
                  f'\'{mySQL_string}\'')

    def get_results(self, auto_dict={}):
        """
        Get result which matches given dictionary. if date is given, can return
        row id or if row id is given in dictionary, it return all entries of
        row id.
        """
        mySQL_string = 'SELECT * FROM result'
        if len(auto_dict) != 0:
            mySQL_string += ' WHERE '
            counter = 0
            for key, value in auto_dict.iteritems():
                if value == 'None':
                    mySQL_string += "%s IS NULL" % (str(key))
                else:
                    k = str(key)
                    v = str(value)
                    v = v.replace('\\', '\\\\')  # handles backslash
                    v = v.replace('\'', '\'\'')  # handles single quotes
                    mySQL_string += "%s='%s'" % (k, v)
                counter += 1
                if (counter != len(auto_dict)):
                    mySQL_string += ' and '
        # try:
        self.cursor.execute(mySQL_string)
        column = [str(i[0]) for i in self.cursor.description]
        # result = self.cursor.fetchall()
        # print(result)
        result = [str(i) for i in self.cursor.fetchone()]
        tmp = zip(column, result)
        result_dict = dict(tmp)
        return result_dict
        # except Exception:
        #     print("Error(%s): Can't get the result for mySQL_string: %s"
        #         % (self.notice, mySQL_string))

    def insert_results(self, auto_dict):
        """
        Insert results into database with provided dictionary
             if successful, return row_id of inserted row.
             if error, returns sql_string with column names.
        """
        mySQL_ins_string = 'insert into result ('
        counter = 0
        for key in auto_dict.keys():
            counter += 1
            mySQL_ins_string += '%s' % (key)
            if (counter != len(auto_dict)):
                mySQL_ins_string += ', '
        mySQL_ins_string += ') values ('
        counter = 0
        for value in auto_dict.values():
            counter += 1
            value = str(value)
            value = value.replace('\\', '\\\\')  # handles backslash
            value = value.replace('\'', '\'\'')  # handles single quotes
            mySQL_ins_string += '\'%s\'' % (value)
            if (counter != len(auto_dict)):
                mySQL_ins_string += ', '
        mySQL_ins_string += ')'
        try:
            ins_count = self.cursor.execute(mySQL_ins_string)
            row_id = 0
            row_id = self.cursor.lastrowid
            return f'Info({self.notice}): {ins_count} entry(s) is added. counter: {row_id}'
        except Exception:
            msg = 'Can\'t insert result into database, mySQL_ins_string: {mySQL_ins_string}'
            print(f'Error({self.notice}): {msg}')
            for key in auto_dict.keys():
                if (0 == self.cursor.execute(
                        f'SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '
                        f'"result" and COLUMN_NAME = "{key}"')):
                    print(f'Error({self.notice}): Can\'t insert result, \'{key}\' '
                          'is not column name.')
            raise Exception(msg)

    def list_all_columns(self):
        """
        List all columns name available for entries in database.
            if error, return msg.
        """
        mySQL_string = 'select * from result'
        try:
            self.cursor.execute(mySQL_string)
            field_names = [str(i[0]) for i in self.cursor.description]
            return sorted(field_names)
        except Exception:
            print(f'Error({self.notice}): Can\'t get the list of all columns')

    def update_results(self, auto_dict):
        """
        Update results into database with provided dictionary
             if successful, return 1
             if error, returns sql_string with column names.
        """
        try:
            row_id = auto_dict['COUNTER']
        except Exception:
            msg = f'Error({self.notice}): COUNTER value is empty. Requires dict w/ row_id'
            return msg

        auto_dict_get = self.get_results({'COUNTER': row_id})

        items2update = {}
        for x in auto_dict.items():
            if x not in auto_dict_get.items():
                k = x[0]
                v = x[1]
                v = str(v)
                v = v.replace('\\', '\\\\')  # handles backslash
                v = v.replace('\'', '\'\'')  # handles single quotes
                items2update[k] = v
        mySQL_string = 'UPDATE result SET '
        i = 0
        for k, v in items2update.iteritems():
            i += 1
            mySQL_string += k + "='" + v + "'"
            if (i != len(items2update)):
                mySQL_string += ", "
        mySQL_string += " WHERE COUNTER="+"'"+auto_dict['COUNTER']+"'"

        try:
            _ = self.cursor.execute(mySQL_string)
            time.sleep(1)
            msg = (f'Info({self.notice}): {len(items2update)} field(s) is updated for counter: '
                   f'{row_id}; {items2update})')
            return msg
        except Exception:
            msg = f'Error({self.notice}): Can\'t update result, mySQL_string: {mySQL_string}'
            print(msg)
            raise Exception(msg)


def convert_Bytes(bytes, to):
    """Convert bytes to megabytes, etc.
    print('mb= ' + str(bytesto(314575262000000, 'm'))) ==> mb= 300002347.946
    """
    a = {
        'KB': 1,
        'MB': 2,
        'GB': 3,
        'TB': 4,
        'PB': 5,
        'EB': 6
    }
    bsize = 1024
    r = float(bytes)
    for i in range(a[to]):
        r = r / bsize
    return int(r)


def convert_Dict_fromOStoAR(osDict):
    """ Convert OmniScript dict to AutoResult dict """
    arDict = {}
    mem_ttl_phy = format(convert_Bytes(osDict['memory_total_physical'], 'MB'), ', d')
    mem_avl_phy = format(convert_Bytes(osDict['memory_available_physical'], 'MB'), ', d')
    disk_ttl = format(convert_Bytes(osDict['storage_total'], 'GB'), ', d')
    _ = format(convert_Bytes(osDict['storage_used'], 'GB'), ', d')
    disk_avl = format(convert_Bytes(osDict['storage_total']-osDict['storage_used'], 'GB'), ', d')
    arDict['MEMORY'] = str(mem_ttl_phy)+" MB Total Phys; "+str(mem_avl_phy)+" MB Avail Phys"
    arDict['ENGINE_DISKSPACE'] = str(disk_ttl)+" GB Total; "+str(disk_avl)+" GB Avail"
    arDict['ENGINE_CPU'] = (f'{re.sub(" +", " ", osDict["cpu_type"])}'
                            f' (CPU Count: {osDict["cpu_count"]})')
    arDict['ENGINE_NAME'] = osDict['name']
    arDict['ENGINE_OS'] = osDict['os']
    arDict['ENGINE_MKT_BUILD'] = osDict['product_version']
    arDict['ENGINE_BUILD'] = osDict['file_version']
    arDict['ENGINE_PLATFORM'] = osDict['platform']
    arDict['ENGINE_TYPE'] = osDict['engine_type']
    return arDict


if __name__ == "__main__":
    AR = AUTORESULT()
    AR.connect_db()

    # Create and Modify entry in database
#     AR_dict = {}
#     AR_dict['CONTACT'] = 'Tom1'
#     AR_dict['TEST_TYPE'] ='cdt'
#     AR_dict['DATE'] =  datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#     AR_dict['TEST_CASE_DURATION'] = '9999'
#     print(AR.insert_results(AR_dict))
#
#     AR_dict_ori = AR.get_results(AR_dict)
#     AR_dict_tmp = AR_dict_ori.copy()
#     AR_dict_tmp['TESTCASE_NUM'] = '12345' # add one entry
#     AR_dict_tmp['TEST_TYPE'] = 'qdt' # update one entry
#     AR_dict_tmp['CONTACT'] = 'Tom2' # update one entry
#     AR_dict_tmp['TEST_CASE_DURATION'] = '' # delete one entry
#     print(AR.update_results(AR_dict_tmp))
#
#     AR_dict_fin = AR.get_results(AR_dict_tmp)
#     for i in ['COUNTER','TESTCASE_NUM','TEST_TYPE','CONTACT','DATE', 'TEST_CASE_DURATION']:
#         print("For key:%s, before:%s and after:%s") % (i, AR_dict_ori[i], AR_dict_fin[i])
