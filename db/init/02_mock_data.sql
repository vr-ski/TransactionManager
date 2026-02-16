-- ============================
-- Languages
-- ============================

INSERT INTO languages (language_code, name)
VALUES
    ('en', 'English'),
    ('bg', 'Bulgarian');

-- ============================
-- Users
-- ============================

INSERT INTO users (username, password_hash)
VALUES
  ('keyuser', '$2b$12$w2BLgLMD9xieiiAN0Bm26uKZ/9koOYg2oXuc3Ivkdlb.q1MYBNMEW'),
  ('client', '$2b$12$w2BLgLMD9xieiiAN0Bm26uKZ/9koOYg2oXuc3Ivkdlb.q1MYBNMEW');

-- ============================
-- Contractors
-- ============================

INSERT INTO contractors (user_id, name)
VALUES
  (1, 'Hristo Botev'),
  (1, 'Ivan Vazov'),
  (2, 'Lyuben Karavelov'),
  (2, 'Petko Slaveykov');

-- ============================
-- Transaction Statuses
-- ============================

INSERT INTO transaction_statuses (code)
VALUES
  ('SENT'),
  ('RECEIVED'),
  ('PAID');

-- Colors
INSERT INTO transaction_status_colors (status_id, color)
VALUES
  (1, 'red'),
  (2, 'yellow'),
  (3, 'green');

-- English translations
INSERT INTO transaction_status_translations (status_id, language_code, display_name)
VALUES
  (1, 'en', 'Sent'),
  (2, 'en', 'Received'),
  (3, 'en', 'Paid');

-- Bulgarian translations
INSERT INTO transaction_status_translations (status_id, language_code, display_name)
VALUES
  (1, 'bg', 'Изпратено'),
  (2, 'bg', 'Получено'),
  (3, 'bg', 'Платено');

-- ============================
-- Transaction Types
-- ============================

INSERT INTO transaction_types (code)
VALUES
  ('CARD_PAYMENT'),
  ('ONLINE_TRANSFER'),
  ('GENERIC_TRANSACTION');

-- English translations
INSERT INTO transaction_type_translations (transaction_type_id, language_code, display_name)
VALUES
  (1, 'en', 'Card Payment'),
  (2, 'en', 'Online Transfer'),
  (3, 'en', 'Transaction');

-- Bulgarian translations
INSERT INTO transaction_type_translations (transaction_type_id, language_code, display_name)
VALUES
  (1, 'bg', 'Плащане с карта'),
  (2, 'bg', 'Онлайн превод'),
  (3, 'bg', 'Транзакция');

-- ============================
-- Transactions (sample)
-- ============================

INSERT INTO transactions (
    user_id,
    contractor_from_id,
    contractor_to_id,
    amount,
    transaction_type_id,
    status_id
)
VALUES
  (1, 1, 3, 50.00, 1, 3),  -- Hristo → Karavelov, Card Payment, Paid
  (2, 3, 1, 20.00, 2, 1),  -- Karavelov → Hristo, Online Transfer, Sent
  (1, 2, 4, 75.00, 3, 2),  -- Vazov → Slaveykov, Generic, Received
  (2, 4, 2, 15.00, 1, 2);  -- Slaveykov → Vazov, Card Payment, Received

-- ============================
-- Additional Sample Transactions
-- ============================

INSERT INTO transactions (
    user_id,
    contractor_from_id,
    contractor_to_id,
    amount,
    transaction_type_id,
    status_id
)
VALUES
  -- User 1 sending to User 2 contractors
  (1, 1, 3, 32.50, 1, 1),
  (1, 1, 4, 120.00, 2, 2),
  (1, 2, 3, 18.75, 3, 3),
  (1, 2, 4, 250.00, 1, 1),

  -- User 2 sending to User 1 contractors
  (2, 3, 1, 44.20, 2, 2),
  (2, 3, 2, 10.00, 3, 3),
  (2, 4, 1, 99.99, 1, 1),
  (2, 4, 2, 15.50, 2, 2),

  -- Mixed amounts and statuses
  (1, 1, 3, 5.00, 3, 2),
  (1, 2, 4, 8.40, 1, 3),
  (2, 3, 1, 300.00, 2, 1),
  (2, 4, 2, 75.25, 3, 2),

  -- Higher-value transactions
  (1, 1, 4, 450.00, 1, 3),
  (2, 3, 2, 520.00, 2, 1),
  (1, 2, 3, 610.00, 3, 2),

  -- Small micro‑transactions
  (2, 4, 1, 2.99, 1, 3),
  (1, 1, 3, 1.50, 2, 2),
  (1, 2, 4, 3.25, 3, 1),

  -- More variety
  (2, 3, 1, 42.42, 1, 2),
  (1, 1, 4, 77.77, 2, 3);


-- ============================
-- Transaction diff dates
-- ============================

INSERT INTO transactions (
    user_id,
    contractor_from_id,
    contractor_to_id,
    amount,
    transaction_type_id,
    status_id,
    created_at,
    updated_at
)
VALUES
  -- User 1 transactions (varied dates)
  (1, 1, 3, 50.00, 1, 3, TIMESTAMP '2026-02-15 09:23:00', TIMESTAMP '2026-02-15 09:23:00'),
  (1, 2, 4, 75.00, 3, 2, TIMESTAMP '2026-02-10 14:15:00', TIMESTAMP '2026-02-10 14:15:00'),
  (1, 1, 4, 450.00, 1, 3, TIMESTAMP '2026-01-28 11:45:00', TIMESTAMP '2026-01-28 11:45:00'),
  (1, 1, 3, 32.50, 1, 1, TIMESTAMP '2026-01-20 16:30:00', TIMESTAMP '2026-01-20 16:30:00'),
  (1, 1, 4, 120.00, 2, 2, TIMESTAMP '2026-01-15 10:00:00', TIMESTAMP '2026-01-15 10:00:00'),
  (1, 2, 3, 18.75, 3, 3, TIMESTAMP '2026-01-05 08:20:00', TIMESTAMP '2026-01-05 08:20:00'),
  (1, 2, 4, 250.00, 1, 1, TIMESTAMP '2025-12-28 13:10:00', TIMESTAMP '2025-12-28 13:10:00'),
  (1, 1, 3, 5.00, 3, 2, TIMESTAMP '2025-12-20 17:45:00', TIMESTAMP '2025-12-20 17:45:00'),
  (1, 2, 4, 8.40, 1, 3, TIMESTAMP '2025-12-15 09:30:00', TIMESTAMP '2025-12-15 09:30:00'),
  (1, 1, 4, 77.77, 2, 3, TIMESTAMP '2025-12-10 12:00:00', TIMESTAMP '2025-12-10 12:00:00'),
  (1, 2, 3, 610.00, 3, 2, TIMESTAMP '2025-12-05 14:25:00', TIMESTAMP '2025-12-05 14:25:00'),
  (1, 1, 3, 1.50, 2, 2, TIMESTAMP '2025-12-01 10:05:00', TIMESTAMP '2025-12-01 10:05:00'),
  (1, 2, 4, 3.25, 3, 1, TIMESTAMP '2025-11-28 16:40:00', TIMESTAMP '2025-11-28 16:40:00'),

  -- User 2 transactions
  (2, 3, 1, 20.00, 2, 1, TIMESTAMP '2026-02-14 08:00:00', TIMESTAMP '2026-02-14 08:00:00'),
  (2, 4, 2, 15.00, 1, 2, TIMESTAMP '2026-02-13 18:30:00', TIMESTAMP '2024-02-13 18:30:00'),
  (2, 3, 1, 44.20, 2, 2, TIMESTAMP '2026-02-12 11:15:00', TIMESTAMP '2024-04-12 11:15:00'),
  (2, 3, 2, 10.00, 3, 3, TIMESTAMP '2026-02-11 09:45:00', TIMESTAMP '2025-06-11 09:45:00'),
  (2, 4, 1, 99.99, 1, 1, TIMESTAMP '2026-02-10 20:00:00', TIMESTAMP '2024-06-10 20:00:00'),
  (2, 4, 2, 15.50, 2, 2, TIMESTAMP '2026-02-09 13:20:00', TIMESTAMP '2023-03-09 13:20:00'),
  (2, 3, 1, 300.00, 2, 1, TIMESTAMP '2026-02-08 10:30:00', TIMESTAMP '2023-06-08 10:30:00'),
  (2, 4, 2, 75.25, 3, 2, TIMESTAMP '2026-02-07 15:45:00', TIMESTAMP '2026-02-07 15:45:00'),
  (2, 3, 2, 520.00, 2, 1, TIMESTAMP '2026-02-06 12:10:00', TIMESTAMP '2026-02-06 12:10:00'),
  (2, 4, 1, 2.99, 1, 3, TIMESTAMP '2026-02-05 09:00:00', TIMESTAMP '2026-02-05 09:00:00'),
  (2, 3, 1, 42.42, 1, 2, TIMESTAMP '2026-02-04 17:25:00', TIMESTAMP '2026-02-04 17:25:00'),
  (2, 4, 2, 75.25, 3, 2, TIMESTAMP '2026-02-03 11:50:00', TIMESTAMP '2026-02-03 11:50:00'),
  (2, 3, 1, 300.00, 2, 1, TIMESTAMP '2026-02-02 14:35:00', TIMESTAMP '2026-02-02 14:35:00'),
  (2, 4, 2, 15.50, 2, 2, TIMESTAMP '2026-02-01 08:55:00', TIMESTAMP '2026-02-01 08:55:00'),

  -- Mixed older transactions
  (1, 1, 3, 50.00, 1, 3, TIMESTAMP '2025-11-15 10:00:00', TIMESTAMP '2025-11-15 10:00:00'),
  (2, 3, 1, 20.00, 2, 1, TIMESTAMP '2025-11-10 11:00:00', TIMESTAMP '2025-11-10 11:00:00'),
  (1, 2, 4, 75.00, 3, 2, TIMESTAMP '2025-11-05 12:00:00', TIMESTAMP '2025-11-05 12:00:00'),
  (2, 4, 2, 15.00, 1, 2, TIMESTAMP '2025-10-30 13:00:00', TIMESTAMP '2025-10-30 13:00:00');
