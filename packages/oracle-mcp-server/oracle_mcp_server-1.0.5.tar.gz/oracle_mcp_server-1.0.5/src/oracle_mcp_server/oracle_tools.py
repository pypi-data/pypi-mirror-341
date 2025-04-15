import oracledb
import asyncio
import os
import logging
import datetime

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

connection_string = ""
lib_dir=""
pool = None

def write_log(message):
    # 用追加模式写入，避免覆盖旧日志
    with open('D://app.log', 'a', encoding='utf-8') as f:
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] {message}\n"
        f.write(log_entry)
# 初始化Oracle客户端和连接池
async def init_pool():
    global pool
    if pool is None:
        try:
            logger.debug("开始初始化连接池")
            write_log("开始初始化连接池")
            write_log(f"连接参数:{connection_string}")
            write_log(f"lib_dir:{lib_dir}")
            # 解析连接字符串
            user, host = connection_string.split('@')
            username, password = user.split('/')
            hostname, service = host.split('/')
            hostname, port = hostname.split(':')
            
            logger.debug(f"连接参数: host={hostname}, port={port}, service={service}, user={username}")
            
            oracledb.init_oracle_client(lib_dir=lib_dir)
            logger.debug("Oracle客户端初始化成功")
            
            # 创建连接池
            pool = await asyncio.to_thread(
                oracledb.create_pool,
                user=username,
                password=password,
                dsn=f"{hostname}:{port}/{service}",
                min=2,
                max=10,
                increment=1,
                getmode=oracledb.POOL_GETMODE_WAIT
            )
            logger.info("数据库连接池初始化成功，最小连接数: 2, 最大连接数: 10")
        except Exception as e:
            logger.error(f"连接池初始化失败: {str(e)}", exc_info=True)
            raise

async def list_tables() -> list:
    tables = []
    try:
        write_log(f"list_tables:1")
        # 在单独的线程中运行数据库操作
        def db_operation():
            result_tables = []
            with pool.acquire() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT table_name FROM user_tables ORDER BY table_name")
                for row in cursor:
                    result_tables.append(row[0])
            return '\n'.join(result_tables)

        return await asyncio.to_thread(db_operation)
    except oracledb.DatabaseError as e:
        print('Error occurred:', e)
        write_log(f"list_tables:{e}")
        return str(e)

async def describe_table(table_name: str) -> str:
    try:
        # 在单独的线程中运行数据库操作
        def db_operation(table):
            with pool.acquire() as conn:
                cursor = conn.cursor()

                # Create CSV headers
                result = [
                    "COLUMN_NAME,DATA_TYPE,NULLABLE,DATA_LENGTH,PRIMARY_KEY,FOREIGN_KEY"]

                # Get primary key columns
                pk_columns = []
                cursor.execute(
                    """
                    SELECT cols.column_name
                    FROM all_constraints cons, all_cons_columns cols
                    WHERE cons.constraint_type = 'P'
                    AND cons.constraint_name = cols.constraint_name
                    AND cons.owner = cols.owner
                    AND cols.table_name = :table_name
                    """,
                    table_name=table.upper()
                )
                for row in cursor:
                    pk_columns.append(row[0])

                # Get foreign key columns and references
                fk_info = {}
                cursor.execute(
                    """
                    SELECT a.column_name, c_pk.table_name as referenced_table, b.column_name as referenced_column
                    FROM all_cons_columns a
                    JOIN all_constraints c ON a.owner = c.owner AND a.constraint_name = c.constraint_name
                    JOIN all_constraints c_pk ON c.r_owner = c_pk.owner AND c.r_constraint_name = c_pk.constraint_name
                    JOIN all_cons_columns b ON c_pk.owner = b.owner AND c_pk.constraint_name = b.constraint_name
                    WHERE c.constraint_type = 'R'
                    AND a.table_name = :table_name
                    """,
                    table_name=table.upper()
                )
                for row in cursor:
                    fk_info[row[0]] = f"{row[1]}.{row[2]}"

                # Get main column information
                cursor.execute(
                    """
                    SELECT column_name, data_type, nullable, data_length 
                    FROM user_tab_columns 
                    WHERE table_name = :table_name 
                    ORDER BY column_id
                    """,
                    table_name=table.upper()
                )

                rows_found = False
                for row in cursor:
                    rows_found = True
                    column_name = row[0]
                    data_type = row[1]
                    nullable = row[2]
                    data_length = str(row[3])
                    is_pk = "YES" if column_name in pk_columns else "NO"
                    fk_ref = fk_info.get(column_name, "NO")

                    # Format as CSV row
                    result.append(
                        f"{column_name},{data_type},{nullable},{data_length},{is_pk},{fk_ref}")

                if not rows_found:
                    return f"Table {table} not found or has no columns."

                return '\n'.join(result)

        return await asyncio.to_thread(db_operation, table_name)
    except oracledb.DatabaseError as e:
        print('Error occurred:', e)
        return str(e)

async def read_query(query: str) -> str:
    try:
        # Check if the query is a SELECT statement
        if not query.strip().upper().startswith('SELECT'):
            return "Error: Only SELECT statements are supported."

        # 在单独的线程中运行数据库操作
        def db_operation(query):
            with pool.acquire() as conn:
                cursor = conn.cursor()
                cursor.execute(query)  # Execute query first

                # Get column names after executing the query
                columns = [col[0] for col in cursor.description]
                result = [','.join(columns)]  # Add column headers

                # Process each row
                for row in cursor:
                    # Convert each value in the tuple to string
                    string_values = [
                        str(val) if val is not None else "NULL" for val in row]
                    result.append(','.join(string_values))

                return '\n'.join(result)

        return await asyncio.to_thread(db_operation, query)
    except oracledb.DatabaseError as e:
        print('Error occurred:', e)
        return str(e)

# 关闭连接池
async def close_pool():
    global pool
    if pool:
        await asyncio.to_thread(pool.close)
        print("数据库连接池已关闭")
        pool = None

if __name__ == "__main__":
    # Create and run the async event loop
    async def main():
        # 初始化连接池
        await init_pool()
        #await list_tables()
        # try:
            # print(await list_tables())
        print(await describe_table('CONTACT'))
        # finally:
        #     await close_pool()

    asyncio.run(main())
