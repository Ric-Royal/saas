import mongoose from 'mongoose';
import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';

export interface User extends mongoose.Document {
  username: string;
  email: string;
  password: string;
  name: string;
  bio?: string;
  avatar?: string;
  isAdmin: boolean;
  generateAuthToken: () => Promise<string>;
  comparePassword: (password: string) => Promise<boolean>;
}

const userSchema = new mongoose.Schema<User>({
  username: {
    type: String,
    required: true,
    unique: true,
    trim: true,
  },
  email: {
    type: String,
    required: true,
    unique: true,
    trim: true,
    lowercase: true,
  },
  password: {
    type: String,
    required: true,
    minlength: 8,
  },
  name: {
    type: String,
    required: true,
    trim: true,
  },
  bio: {
    type: String,
    trim: true,
  },
  avatar: {
    type: String,
  },
  isAdmin: {
    type: Boolean,
    default: false,
  },
}, {
  timestamps: true,
});

// Hash password before saving
userSchema.pre('save', async function(next) {
  const user = this;
  if (user.isModified('password')) {
    user.password = await bcrypt.hash(user.password, 10);
  }
  next();
});

// Generate JWT token
userSchema.methods.generateAuthToken = async function() {
  const user = this;
  const token = jwt.sign(
    { id: user._id.toString() },
    process.env.JWT_SECRET || 'your-secret-key',
    { expiresIn: '7d' }
  );
  return token;
};

// Compare password
userSchema.methods.comparePassword = async function(password: string) {
  const user = this;
  return bcrypt.compare(password, user.password);
};

// Remove sensitive data when converting to JSON
userSchema.methods.toJSON = function() {
  const user = this;
  const userObject = user.toObject();
  delete userObject.password;
  return userObject;
};

export const User = mongoose.model<User>('User', userSchema); 