
'''Handles the table structure'''

# database specific
def show_all_tables(conn):
    #  all table names in our db
    pass
def is_table_exists(conn,table):
    pass
def create_table(conn,table,struct):
    pass

def _desc_table(conn , table):
    pass
def _show_create_table(conn,table):
    pass # to find fk_values if lost
# takes conn from caller (depends on executor (utils))
def _alter_table(conn,table_name,remaining_query):
    # sample struct 'alter table {table_name} {remaining_query}
    pass
def _truncate_table(conn , table):
    pass

# alter specific (Required add / drop in query)
# no any existence required except the table itself
def _is_column_exists(conn,table,column):
    pass
def _is_constraint_exists(conn,table,constraint):
    pass
def rename_table(conn,old_name,new_name):
    pass

def change_auto_increment(conn,table,auto_increment_value):
    # sample 'auto_increment = value ' reset send to alter
    pass 
def drop_table(conn,table_name):
    pass

# column specific
# no column existence required
def add_column(conn,table,new_column_config,before=None,after=None):
    #  add new column (whole name + config)
    pass
# column existence also required
def modify_column(conn,table ,old_column_name,new_config):
    # change (column_config only ) 
    pass
def change_column(conn,table,old_column_name,new_column_config):
    #  change (name + config ) 
    pass
def drop_column(conn,table,column):
    pass

# constraints specific 
def _add_constraint(conn,table,constraint_config):
    #  sample alter table {table} add constraint {constraint_config}
    pass


def add_primary_key(conn,table,column):
    #sample  'primary key (name)' 
    pass
def add_unique_key(conn,key_name,table,column):
    # sample 'unique (column)'
    pass
def add_foreign_key(conn,table,key_name,column,reference):
    #  foreign key {key_name} (column) references (references)
     # fk_name can be fk_{column_name} for easy access
    pass
def add_index(conn,index_name,table,column):
    # 
    pass
def drop_primary_key(conn,table):
    #sample  'primary key' 
    pass
def drop_unique_key(conn,table,key_name):
    # sample 'unique (column)'
    pass
def drop_foreign_key(conn,table,fk_name):
    #  foreign key (column) references (references)
    # fk_name can be fk_{column_name} for easy access
    pass
def drop_index(conn,table,index_name):
    #  'index {column}' 
    pass
