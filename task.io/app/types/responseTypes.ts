// app/types/responseTypes.ts

export interface CustomError {
    detail?: string; // Response may be undefined,
    status?: string; // Response may be undefined
}

export interface ImageResponse {
  id?: string;
  message?: string;
  code?: string;
}