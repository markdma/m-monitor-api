# 主机组
ALTER TABLE falcon_portal.grp
ADD COLUMN tenant_id VARCHAR ( 32 ),
ADD COLUMN project_id VARCHAR ( 32 ),
ADD COLUMN update_user VARCHAR ( 64 ),
ADD COLUMN update_at TIMESTAMP;

# 主机
ALTER TABLE falcon_portal.host
ADD COLUMN update_user VARCHAR ( 32 );

# 模板
ALTER TABLE falcon_portal.tpl
ADD COLUMN update_user VARCHAR ( 64 ),
ADD COLUMN update_at TIMESTAMP,
ADD COLUMN tenant_id VARCHAR ( 32 ),
ADD COLUMN project_id VARCHAR ( 32 );


# 单模板
ALTER TABLE falcon_portal.host_tpl
ADD COLUMN tenant_id VARCHAR ( 32 ),
ADD COLUMN project_id VARCHAR ( 32 ),
ADD COLUMN update_user VARCHAR ( 64 ),
ADD COLUMN update_at TIMESTAMP;

# 策略
ALTER TABLE falcon_portal.strategy
ADD COLUMN tenant_id VARCHAR ( 32 ),
ADD COLUMN project_id VARCHAR ( 32 );

# 行动
ALTER TABLE falcon_portal.action
ADD COLUMN tenant_id VARCHAR ( 32 ),
ADD COLUMN project_id VARCHAR ( 32 );

# 自定义上报 主机
ALTER TABLE falcon_portal.host
ADD COLUMN tenant_id VARCHAR ( 32 ),
ADD COLUMN project_id VARCHAR ( 32 ),
ADD COLUMN create_user VARCHAR ( 64 ),
ADD COLUMN create_at TIMESTAMP;

# 自定义上报 custom
ALTER TABLE falcon_portal.custom
ADD COLUMN tenant_id VARCHAR ( 32 ),
ADD COLUMN project_id VARCHAR ( 32 );

