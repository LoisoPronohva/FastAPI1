-- Создание тестовых пользователей (пароль для всех: password123)
INSERT INTO users (username, email, hashed_password, role) VALUES
('admin', 'admin@example.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'admin'),
('user1', 'user1@example.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'user'),
('user2', 'user2@example.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'user')
ON CONFLICT (username) DO NOTHING;

-- Создание тестовых объявлений
INSERT INTO advertisements (title, description, price, author, owner_id) VALUES
('Продам ноутбук', 'Отличный ноутбук в идеальном состоянии', 45000.0, 'Иван', 2),
('Куплю велосипед', 'Ищу горный велосипед, б/у', 15000.0, 'Петр', 3),
('Сдам квартиру', '1-комнатная квартира в центре', 30000.0, 'Анна', 2),
('Продам iPhone 13', 'Телефон в отличном состоянии, с гарантией', 65000.0, 'Сергей', 3)
ON CONFLICT DO NOTHING;