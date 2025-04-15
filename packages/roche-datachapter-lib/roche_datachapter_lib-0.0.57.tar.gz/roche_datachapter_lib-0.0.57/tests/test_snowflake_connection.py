from roche_datachapter_lib.db_config import DB_CONFIG

query = "SELECT COUNT(*) FROM BUSINESS_CONSUMABLES_MATERIALS_PRICELIST"

df = DB_CONFIG.execute_custom_select_query(
    query=query,
    p_bind='snowflake_default',
    snowflake_ctx={
        "db":        "AR_PRICELIST_DEV",
        "schema":    "BUSINESS_DV_AR_PRICELIST",
        "warehouse": "WH_AR_PRICELIST_01"
    }
)
