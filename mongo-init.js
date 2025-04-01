// 切换到情感分析引擎数据库
db = db.getSiblingDB('emotion_db');

// 创建必要的集合
db.createCollection('users');
db.createCollection('emotion_records');
db.createCollection('user_profiles');
db.createCollection('alerts');
db.createCollection('social_emotion_records');
db.createCollection('user_behaviors');

// 创建索引
db.users.createIndex({ "username": 1 }, { unique: true });
db.users.createIndex({ "email": 1 }, { unique: true });
db.emotion_records.createIndex({ "user_id": 1, "timestamp": -1 });
db.user_profiles.createIndex({ "user_id": 1 }, { unique: true });
db.alerts.createIndex({ "user_id": 1, "created_at": -1 });
db.alerts.createIndex({ "status": 1 });
db.social_emotion_records.createIndex({ "user_id": 1, "timestamp": -1 });
db.social_emotion_records.createIndex({ "target_user_id": 1, "timestamp": -1 });
db.user_behaviors.createIndex({ "user_id": 1, "timestamp": -1 });

// 添加管理员用户示例（密码需在生产环境中修改）
// 默认密码：admin123
db.users.insertOne({
    username: "admin",
    email: "admin@example.com",
    hashed_password: "$2b$12$8sqU.2FXYJzRFO0xKWFj6eXky2XHl5EjNiME0z6jiYCYLcV8qsTp6", // admin123的bcrypt哈希
    role: "admin",
    is_active: true,
    created_at: new Date(),
    updated_at: new Date()
});

print("数据库初始化完成"); 