<?php
// 資料庫配置
$servername = "34.28.106.5"; // 或者使用你的實際主機名
$username = "root"; // 你的資料庫用戶名
$password = "#fcu-DBS#"; // 你的資料庫密碼
$dbname = "graphic-linker-423604-v0:us-central1:fcu-database"; // 你的資料庫名稱

// 建立資料庫連接
$conn = new mysqli($servername, $username, $password, $dbname);

// 檢查連接
if ($conn->connect_error) {
    die("連接失敗: " . $conn->connect_error);
}

// SQL 查詢
$sql = "SELECT Name, Identity, Account, Ctfc, password FROM customer"; // 修改為你的資料表和欄位名稱
$result = $conn->query($sql);

// 檢查是否有結果
if ($result->num_rows > 0) {
    // 輸出資料
    while($row = $result->fetch_assoc()) {
        echo "Name: " . $row["Name"]. " - ID: " . $row["Identity"]. " - Account: " . $row["Account"]. $row["Ctfc"]. $row[password]. "<br>";
    }
}
else {
    echo "沒有資料";
}

// 關閉連接
$conn->close();
?>
