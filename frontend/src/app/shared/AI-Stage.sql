-- create the database
CREATE DATABASE aistage;

-- use the database
USE aistage;

-- create the table
CREATE TABLE ContactMessages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--
-- Dumping data for table `contactmessages`
--

INSERT INTO `contactmessages` (`id`, `first_name`, `last_name`, `email`, `message`, `created_at`) VALUES
(1, 'Test', 'User', 'testuser@example.com', 'This is a test message.', '2025-04-01 11:08:45');

--
-- Indexes for table `contactmessages`
--
ALTER TABLE `contactmessages`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for table `contactmessages`
--
ALTER TABLE `contactmessages`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;
COMMIT;