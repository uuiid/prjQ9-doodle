# import script.MySqlComm
# data = 'dubuxiaoyao'
# for i in range(1,13):
#     create_date ="""alter table `ep{:0>3d}`
# add column `infor` varchar(4096) ,
# add column `filetime` datetime default current_timestamp on update current_timestamp """.format(i)
#     script.MySqlComm.inserteCommMysql(data, '', '', create_date)
import script.doodleLog

ta_log = script.doodleLog.ta_log


@script.doodleLog.errorDecorator(ta_log)
def zero_divide():
    taa = {}
    print(taa['da'])

if __name__ == '__main__':
    zero_divide()