import nodemailer from 'nodemailer';
import { verificationEmailTemplate, passwordResetTemplate } from '../templates/emails';

const transporter = nodemailer.createTransport({
  host: process.env.SMTP_HOST,
  port: Number(process.env.SMTP_PORT),
  auth: {
    user: process.env.SMTP_USER,
    pass: process.env.SMTP_PASS,
  },
});

export const sendVerificationEmail = async (to: string, token: string, name: string) => {
  const verificationLink = `${process.env.FRONTEND_URL}/verify-email?token=${token}`;
  const html = verificationEmailTemplate(name, verificationLink);
  
  await transporter.sendMail({
    from: process.env.SMTP_FROM,
    to,
    subject: 'Verify your email',
    html,
  });
};

export const sendPasswordResetEmail = async (to: string, token: string, name: string) => {
  const resetLink = `${process.env.FRONTEND_URL}/reset-password?token=${token}`;
  const html = passwordResetTemplate(name, resetLink);

  await transporter.sendMail({
    from: process.env.SMTP_FROM,
    to,
    subject: 'Reset your password',
    html,
  });
}; 