<?php
// Debugging: Check if POST data is received
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    if (empty($_POST)) {
        die("No POST data received. Check your form submission.");
    }

    // Retrieve form data
    $name = $_POST['name'] ?? '';
    $gender = $_POST['gender'] ?? '';
    $qualification = $_POST['qualification'] ?? '';
    $passing_grade = $_POST['passing_grade'] ?? '';

    try {
        // Create or open the SQLite database
        $db = new SQLite3('personal_details.db');

        // Ensure table exists
        $db->exec("CREATE TABLE IF NOT EXISTS personal_details (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            gender TEXT,
            qualification TEXT,
            passing_grade TEXT
        )");

        // Prepare an SQL statement to prevent SQL injection
        $stmt = $db->prepare("INSERT INTO personal_details (name, gender, qualification, passing_grade) VALUES (:name, :gender, :qualification, :passing_grade)");
        
        // Bind parameters
        $stmt->bindValue(':name', $name, SQLITE3_TEXT);
        $stmt->bindValue(':gender', $gender, SQLITE3_TEXT);
        $stmt->bindValue(':qualification', $qualification, SQLITE3_TEXT);
        $stmt->bindValue(':passing_grade', $passing_grade, SQLITE3_TEXT);
        
        // Execute the statement
        if ($stmt->execute()) {
            echo "✅ Data submitted successfully!";
        } else {
            echo "❌ Error: " . $db->lastErrorMsg();
        }

        // Close the database connection
        $db->close();
    } catch (Exception $e) {
        echo "❌ Database error: " . $e->getMessage();
    }
} else {
    echo "❌ Invalid request method.";
}
?>
