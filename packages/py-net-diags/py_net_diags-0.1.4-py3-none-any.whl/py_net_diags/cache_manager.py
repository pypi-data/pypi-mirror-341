import logging

LOG = logging.getLogger("py_net_diags.cache_manager")

class CacheManager:
    def __init__(self, running_in_asio: bool = True, log=None):
        self.tables = {}
        self.running_in_asio = running_in_asio
        self.log = log if log is not None else LOG

    def get_table(self, table_name: str) -> dict:
        self.log.debug(f"Requested cache table: {table_name}")
        if table_name not in self.tables:
            self.tables[table_name] = {}
            self.log.debug(f"Created new cache table: {table_name}")
        else:
            self.log.debug(f"Using existing cache table: {table_name} with {len(self.tables[table_name])} entries")
        return self.tables[table_name]

    def get(self, table_name: str, key):
        table = self.get_table(table_name)
        self.log.debug(f"Cache get for {table_name} with key {key}")
        value = table.get(key)
        if value is None:
            self.log.debug(f"Cache miss for {table_name}:{key}")
            return None
        else:
            self.log.debug(f"Cache hit for {table_name}:{key}")
            if isinstance(value, dict) or isinstance(value, list):
                self.log.debug(f"Value size: {len(str(value))} characters")
            else:
                self.log.debug(f"Value: {value}")
            return value

    def set(self, table_name: str, key, value):
        table = self.get_table(table_name)
        self.log.debug(f"Cache set for {table_name} with key {key}")
        if key in table:
            self.log.debug(f"Overwriting existing cache entry for {table_name}:{key}")
        else:
            self.log.debug(f"Creating new cache entry for {table_name}:{key}")
        
        table[key] = value
        
        if isinstance(value, dict) or isinstance(value, list):
            self.log.debug(f"Stored value size: {len(str(value))} characters")
            if len(table) < 5:  # Only log full tables if they're small
                self.log.debug(f"Table after set: {table}")
            else:
                self.log.debug(f"Table {table_name} now has {len(table)} entries")
                self.log.debug(f"Table keys: {list(table.keys())}")
        else:
            self.log.debug(f"Stored value: {value}")
            self.log.debug(f"Table after set: {table}")

    def delete(self, table_name: str, key):
        self.log.debug(f"Cache delete for {table_name} with key {key}")
        if table_name not in self.tables:
            self.log.warning(f"Attempted to delete from non-existent table: {table_name}")
            return
            
        table = self.get_table(table_name)
        if key in table:
            self.log.debug(f"Deleting cache entry for {table_name}:{key}")
            del table[key]
            self.log.debug(f"Table now has {len(table)} entries")
            if len(table) < 5:  # Only log full tables if they're small
                self.log.debug(f"Table after delete: {table}")
            else:
                self.log.debug(f"Table keys after delete: {list(table.keys())}")
        else:
            self.log.warning(f"Attempted to delete non-existent key: {key} from table: {table_name}")

    def clear(self, table_name: str = None):
        if table_name:
            if table_name in self.tables:
                entry_count = len(self.tables[table_name])
                self.tables[table_name] = {}
                self.log.debug(f"Cleared cache table: {table_name} (removed {entry_count} entries)")
            else:
                self.log.warning(f"Attempted to clear non-existent table: {table_name}")
        else:
            table_count = len(self.tables)
            entry_counts = {name: len(table) for name, table in self.tables.items()}
            total_entries = sum(entry_counts.values())
            self.tables.clear()
            self.log.debug(f"Cleared all cache tables ({table_count} tables, {total_entries} total entries)")
            self.log.debug(f"Cleared tables were: {entry_counts}")
    
    def get_stats(self):
        """Return statistics about the cache contents"""
        stats = {
            "table_count": len(self.tables),
            "tables": {}
        }
        
        for table_name, table in self.tables.items():
            stats["tables"][table_name] = {
                "entry_count": len(table),
                "keys": list(table.keys())
            }
        
        self.log.debug(f"Cache stats: {len(self.tables)} tables with {sum(len(t) for t in self.tables.values())} total entries")
        self.log.debug(f"Detailed cache stats: {stats}")
        return stats
