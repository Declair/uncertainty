#!/usr/bin/python
# -*- coding: UTF-8 -*-
import config
import mysql.connector

loginSql = "SELECT c_account, c_password FROM t_user WHERE c_account = %s"

modelSql = "SELECT n_id, c_project, n_pid FROM t_project"

selectProj = "SELECT n_id, c_project, n_pid FROM t_project where c_project = %s"\
             "and n_pid = %s"

insertProj = "insert into t_project(c_project, n_pid, c_descr) values(%s, %s, %s)"

importSql = "insert into t_file(n_project, c_dir, c_filename, b_pyfile) " \
            "values(%s, %s, %s, %s)"
            
exportSql = "SELECT c_dir, c_filename, b_pyfile FROM t_file WHERE n_project = %s"

insertParam = "insert into model_arg(arg_name, model_id, arg_descr, arg_unit, " \
            "arg_init) values(%s, %s, %s, %s, %s)"

insertVar = "insert into model_arg(arg_name, model_id, arg_descr, arg_unit, " \
            "arg_init, arg_type) values(%s, %s, %s, %s, %s, '0')"

selectModel = "SELECT c_project,c_descr,n_pid FROM t_project WHERE n_id = %s"

selectModelArgs = "SELECT arg_name,arg_descr,arg_init,arg_id FROM model_arg WHERE model_id = %s"\
                  " and (arg_type != 0 or arg_type is NULL) order by arg_id asc"

selectModelVars = "SELECT arg_name,arg_descr,arg_init,arg_id,arg_type FROM model_arg WHERE model_id = %s"\
                  " and arg_type = 0 order by arg_id asc"

selectModelOutputArgs = "SELECT op_name,op_descr,op_id FROM t_output_param WHERE model_id = %s order by op_id asc"

deleteModel = "DELETE FROM t_project WHERE n_id = %s"

deleteModelArgs = "DELETE FROM model_arg WHERE model_id = %s"

deleteModelOutputArgs = "DELETE FROM t_output_param WHERE model_id = %s"

# selectModel = "SELECT c_project,c_descr,n_pid FROM t_project WHERE n_id = %s"

# selectModelArgs = "SELECT arg_name,arg_id,arg_init FROM model_arg WHERE model_id = %s"

# deleteModel = "DELETE FROM t_project WHERE n_id = %s"

# deleteModelArgs = "DELETE FROM model_arg WHERE model_id = %s"

deleteSamplingResult = "DELETE FROM t_sampling_result WHERE r_id in "\
                       "(SELECT arg_id FROM model_arg WHERE model_id = %s)"

model_d_Sql = "SELECT arg_name FROM model_arg ORDER BY arg_id"

get_model_Sql = "SELECT m.model_name, a.arg_name, a.dis_type, a.dis_arg FROM model_arg a, model m  WHERE m.model_id = a.model_id AND m.model_name = "

# 连接模型和参数表 查询选中的模型的名称 和其对应的参数名 分布类型 分布参数 参数ID 和 参数类型
get_arg_Sql = "SELECT m.c_project, a.arg_name, a.dis_type, a.dis_arg, a.arg_id ,a.arg_type FROM model_arg a, t_project m  WHERE m.n_id = a.model_id AND m.c_project = "

def selectSql(args=(), sql=''):
    db_config = config.datasourse
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(sql, args)
        record = cursor.fetchall()
    except mysql.connector.Error as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
    return record

def insertSql(args=(), sql=''):
    db_config = config.datasourse
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(sql, args)
        conn.commit()
    except mysql.connector.Error as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


def clear_sampling_result():
    query = "delete from  t_sampling_result"

    db_config = config.datasourse

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
    except mysql.connector.Error as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

# 传入参数名和所有抽样结果 循环写入
def insert_sampling_result(arg_names,results):
    db_config = config.datasourse

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        j = 0
        for result in results:
            for i in result:
                query = "insert into t_sampling_result(r_value,arg_name) values(%s,%s)"
                args = (float(i), arg_names[j])
                cursor.execute(query, args)
            j += 1
            conn.commit()
    except mysql.connector.Error as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

def deleteSql(args=(), sql=''):
    db_config = config.datasourse
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(sql, args)
        conn.commit()
    except mysql.connector.Error as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

def show_sampling_result(name):
    query = "select r_value from t_sampling_result  where arg_name = '" + name + "' order by r_id;"
    try:
        db_config = config.datasourse
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(query)
        # 获取所有记录列表
        results = cursor.fetchall()
        return results

    except mysql.connector.Error as e:
        print(e)
    cursor.close()
    conn.close()


def show_sampling_result_with_type(name):
    query = "select r_value from t_sampling_result  where arg_name = '" + name + "' order by r_id;"
    try:
        db_config = config.datasourse
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(query)
        # 获取所有记录列表
        results = cursor.fetchall()
        return results

    except mysql.connector.Error as e:
        print(e)
    cursor.close()
    conn.close()


def insert_new_model(model_id,inputargs=[],vars = [],outputargs=[] ):
    """保存新建模型数据信息"""
    sql = "insert into model_arg (arg_name,arg_descr,arg_init,model_id) values(%s,%s,%s,%s)"
    sql1 = "insert into model_arg (arg_name,arg_descr,arg_init,arg_type,model_id) values(%s,%s,%s,%s,%s)"
    sql2 = "insert into t_output_param (op_name,op_descr,model_id) values(%s,%s,%s)"
    db_config = config.datasourse
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        """写输入参数信息到数据库"""
        for i in inputargs:
            print i
            i.append(model_id)
            cursor.execute(sql, i)
        """写自变量信息到数据库"""
        for i in vars:
            print i
            i.append(model_id)
            cursor.execute(sql1, i)
        """写输出参数信息到数据库"""
        for i in outputargs:
            i.append(model_id)
            print i
            cursor.execute(sql2, i)

        conn.commit()
    except mysql.connector.Error as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
    return True


def update_model(model_id,inputargs=[],vars = [],outputargs=[] ):
    """更新模型数据信息"""
    sql = "update model_arg set arg_name=%s,arg_descr=%s,arg_init=%s where arg_id=%s and model_id=%s"
    sql1 = "update model_arg set arg_name=%s,arg_descr=%s,arg_init=%s where arg_id=%s and arg_type=%s and model_id=%s"
    sql2 = "update t_output_param set op_name=%s,op_descr=%s where op_id=%s and model_id=%s"
    db_config = config.datasourse
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        """写输入参数信息到数据库"""
        for i in inputargs:
            print i
            i.append(model_id)
            cursor.execute(sql, i)

        """写自变量信息到数据库"""
        for i in vars:
            print i
            i.append(model_id)
            cursor.execute(sql1, i)

        """写输出参数信息到数据库"""
        for i in outputargs:
            i.append(model_id)
            print i
            cursor.execute(sql2, i)

        conn.commit()
    except mysql.connector.Error as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
    return True