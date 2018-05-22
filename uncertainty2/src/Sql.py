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

model_d_Sql = "SELECT arg_name FROM model_arg ORDER BY arg_id"

get_model_Sql = "SELECT m.model_name, a.arg_name, a.dis_type, a.dis_arg FROM model_arg a, model m  WHERE m.model_id = a.model_id AND m.model_name = "

get_arg_Sql = "SELECT m.c_project, a.arg_name, a.dis_type, a.dis_arg FROM model_arg a, t_project m  WHERE m.n_id = a.model_id AND m.c_project = "

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


def insert_sampling_result(arg_name,result=[] ):
    result = list(result)
    for i in result:
        query = "insert into t_sampling_result(r_value,arg_name) values(%s,%s)"

        args = (float(i),arg_name)
        db_config = config.datasourse

        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            cursor.execute(query, args)
            conn.commit()
        except mysql.connector.Error as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

# def insert_sampling_result_pre(arg_name,result=[] ):
#     result = list(result)
#     for i in result:
#         query = "insert into sampling_result(r_value,arg_name) values(%s,%s)"
#
#         args = (float(i),arg_name)
#         db_config = config.datasourse
#
#         try:
#             conn = mysql.connector.connect(**db_config)
#             cursor = conn.cursor()
#             cursor.execute(query, args)
#             conn.commit()
#         except mysql.connector.Error as e:
#             print(e)
#         finally:
#             cursor.close()
#             conn.close()

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