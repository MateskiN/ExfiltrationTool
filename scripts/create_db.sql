CREATE DATABASE whatsapp_new;
\c whatsapp_new

CREATE SCHEMA whatsapp;

CREATE TABLE whatsapp.Users(
	user_id SERIAL PRIMARY KEY,
	phone_number VARCHAR(255) NOT NULL UNIQUE,
	name VARCHAR(255) NOT NULL,
	profile_picture VARCHAR(255),
	status VARCHAR(255) DEFAULT 'Hey there! I am using this app',
	last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

CREATE TABLE whatsapp.Chats(
	chat_id SERIAL PRIMARY KEY, 
	chat_name VARCHAR(255), 
	is_group BOOLEAN NOT NULL DEFAULT 'False', 
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

CREATE TABLE whatsapp.ChatMembers(
	chat_id INTEGER, 
	user_id INTEGER, 
	is_admin BOOLEAN DEFAULT 'False', 
	joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
	CONSTRAINT fk_chats FOREIGN KEY(chat_id) REFERENCES whatsapp.chats(chat_id), 
	CONSTRAINT fk_users FOREIGN KEY(user_id) REFERENCES whatsapp.users(user_id));

CREATE TABLE whatsapp.Messages(
	message_id SERIAL PRIMARY KEY, 
	chat_id INTEGER NOT NULL, 
	sender_id INTEGER NOT NULL, 
	message_type VARCHAR(255) NOT NULL CHECK(message_type IN ('text', 'image', 'video', 'audio', 'document', 'location', 'contact')), 
	content VARCHAR(255), 
	media_url VARCHAR(255), 
	timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
	is_deleted BOOLEAN DEFAULT 'False', 
	CONSTRAINT fk_chats FOREIGN KEY(chat_id) REFERENCES whatsapp.chats(chat_id), 
	CONSTRAINT fk_senders FOREIGN KEY(sender_id) REFERENCES whatsapp.users(user_id));

CREATE TABLE whatsapp.MessageStatus(
	message_id INTEGER, 
	user_id INTEGER, 
	status VARCHAR(255) NOT NULL CHECK(status IN ('sent', 'delivered', 'read')), 
	updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
	CONSTRAINT fk_messages FOREIGN KEY(message_id) REFERENCES whatsapp.messages(message_id), 
	CONSTRAINT fk_users FOREIGN KEY(user_id) REFERENCES whatsapp.users(user_id));