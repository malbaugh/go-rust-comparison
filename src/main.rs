// main.rs
use axum::{
    routing::{get, post, put, delete},
    extract::{Path, Json, State},
    http::StatusCode,
    Router,
};
use serde::{Deserialize, Serialize};
use std::{collections::HashMap, net::SocketAddr, sync::{Arc, Mutex}};

#[derive(Serialize, Deserialize, Clone)]
struct User {
    id: String,
    name: String,
}

type Db = Arc<Mutex<HashMap<String, User>>>;

#[tokio::main]
async fn main() {
    let db: Db = Arc::new(Mutex::new(HashMap::new()));
    let app = Router::new()
        .route("/users", post(create_user))
        .route("/users/:id", get(get_user).put(update_user).delete(delete_user))
        .with_state(db);

    let addr = SocketAddr::from(([0, 0, 0, 0], 8080));
    axum::serve(tokio::net::TcpListener::bind(addr).await.unwrap(), app).await.unwrap();
}

async fn create_user(
    State(db): State<Db>,
    Json(user): Json<User>,
) -> (StatusCode, Json<User>) {
    let mut store = db.lock().unwrap();
    store.insert(user.id.clone(), user.clone());
    (StatusCode::CREATED, Json(user))
}

async fn get_user(
    Path(id): Path<String>,
    State(db): State<Db>,
) -> Result<Json<User>, StatusCode> {
    let store = db.lock().unwrap();
    store.get(&id).cloned().map(Json).ok_or(StatusCode::NOT_FOUND)
}

async fn update_user(
    Path(id): Path<String>,
    State(db): State<Db>,
    Json(mut user): Json<User>,
) -> Json<User> {
    let mut store = db.lock().unwrap();
    user.id = id.clone();
    store.insert(id, user.clone());
    Json(user)
}

async fn delete_user(
    Path(id): Path<String>,
    State(db): State<Db>,
) -> StatusCode {
    let mut store = db.lock().unwrap();
    store.remove(&id);
    StatusCode::NO_CONTENT
}
