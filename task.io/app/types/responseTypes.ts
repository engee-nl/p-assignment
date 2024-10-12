// app/types/responseTypes.ts

interface CustomError {
    detail?: string; // Response may be undefined,
    status?: string; // Response may be undefined
}

interface ImageResponse {
  id?: string;
  message?: string;
  code?: string;
}