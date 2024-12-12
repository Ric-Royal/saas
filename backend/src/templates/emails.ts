export const verificationEmailTemplate = (name: string, verificationLink: string) => `
<!DOCTYPE html>
<html>
<head>
  <style>
    .container {
      max-width: 600px;
      margin: 0 auto;
      padding: 20px;
      font-family: Arial, sans-serif;
    }
    .button {
      display: inline-block;
      padding: 12px 24px;
      background-color: #4F46E5;
      color: white;
      text-decoration: none;
      border-radius: 6px;
      margin: 20px 0;
    }
    .footer {
      margin-top: 30px;
      font-size: 12px;
      color: #666;
    }
  </style>
</head>
<body>
  <div class="container">
    <h2>Welcome to Our Platform!</h2>
    <p>Hi ${name},</p>
    <p>Thank you for signing up. Please verify your email address by clicking the button below:</p>
    
    <a href="${verificationLink}" class="button">Verify Email</a>
    
    <p>If the button doesn't work, you can also copy and paste this link into your browser:</p>
    <p>${verificationLink}</p>
    
    <div class="footer">
      <p>This link will expire in 24 hours.</p>
      <p>If you didn't create an account, you can safely ignore this email.</p>
    </div>
  </div>
</body>
</html>
`;

export const passwordResetTemplate = (name: string, resetLink: string) => `
<!DOCTYPE html>
<html>
<head>
  <style>
    .container {
      max-width: 600px;
      margin: 0 auto;
      padding: 20px;
      font-family: Arial, sans-serif;
    }
    .button {
      display: inline-block;
      padding: 12px 24px;
      background-color: #4F46E5;
      color: white;
      text-decoration: none;
      border-radius: 6px;
      margin: 20px 0;
    }
    .footer {
      margin-top: 30px;
      font-size: 12px;
      color: #666;
    }
  </style>
</head>
<body>
  <div class="container">
    <h2>Password Reset Request</h2>
    <p>Hi ${name},</p>
    <p>We received a request to reset your password. Click the button below to create a new password:</p>
    
    <a href="${resetLink}" class="button">Reset Password</a>
    
    <p>If the button doesn't work, you can also copy and paste this link into your browser:</p>
    <p>${resetLink}</p>
    
    <div class="footer">
      <p>This link will expire in 1 hour.</p>
      <p>If you didn't request a password reset, you can safely ignore this email.</p>
    </div>
  </div>
</body>
</html>
`; 