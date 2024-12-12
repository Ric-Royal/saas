import mongoose from 'mongoose';

interface IPost {
  title: string;
  content: string;
  author: string;
  tags: string[];
  createdAt: Date;
  updatedAt: Date;
}

interface IPostModel extends mongoose.Model<IPost> {}

const postSchema = new mongoose.Schema<IPost>(
  {
    title: {
      type: String,
      required: true,
      trim: true,
    },
    content: {
      type: String,
      required: true,
    },
    author: {
      type: String,
      required: true,
    },
    tags: [{
      type: String,
      trim: true,
    }],
  },
  {
    timestamps: true,
  }
);

export const Post = mongoose.model<IPost, IPostModel>('Post', postSchema); 