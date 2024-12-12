import { Response } from 'express';

interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: {
    message: string;
    code?: string;
  };
  meta?: {
    page?: number;
    limit?: number;
    total?: number;
  };
}

export const sendSuccess = <T>(
  res: Response,
  data: T,
  statusCode = 200,
  meta?: ApiResponse<T>['meta']
) => {
  const response: ApiResponse<T> = {
    success: true,
    data,
    ...(meta && { meta })
  };
  return res.status(statusCode).json(response);
};

export const sendError = (
  res: Response,
  message: string,
  statusCode = 500,
  code?: string
) => {
  const response: ApiResponse<null> = {
    success: false,
    error: {
      message,
      ...(code && { code })
    }
  };
  return res.status(statusCode).json(response);
}; 