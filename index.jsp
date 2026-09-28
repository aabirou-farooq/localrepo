<%@ page language="java" contentType="text/html; charset=UTF-8" %>

<!DOCTYPE html>
<html>
<head>
    <title>Student Registration</title>

    <style>
        body {
            font-family: Arial;
            margin: 40px;
        }

        .form-box {
            width: 400px;
            padding: 20px;
            border: 1px solid black;
        }

        input, select {
            width: 100%;
            padding: 8px;
            margin: 8px 0;
        }

        input[type="submit"] {
            width: auto;
            cursor: pointer;
        }
    </style>
</head>

<body>

<h1>Student Registration</h1>

<div class="form-box">

<form method="post">

    <label>Student Name:</label>
    <input type="text" name="name" required>

    <label>Course:</label>
    <select name="course">
        <option value="BCA">BCA</option>
        <option value="BSc">BSc</option>
        <option value="BCom">BCom</option>
    </select>

    <label>Marks:</label>
    <input type="number" name="marks" min="0" max="100" required>

    <input type="submit" value="Register">

</form>

</div>

<%
    String name = request.getParameter("name");
    String course = request.getParameter("course");
    String marks = request.getParameter("marks");

    if (name != null && course != null && marks != null) {
%>

    <h2>Registration Successful</h2>

    <p><b>Name:</b> <%= name %></p>
    <p><b>Course:</b> <%= course %></p>
    <p><b>Marks:</b> <%= marks %></p>

<%
    }
%>

</body>
</html>