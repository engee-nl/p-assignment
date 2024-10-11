import axios from 'axios';

// Upload image to the API
export const uploadImage = (formData: FormData) => {
  return axios.post('/api/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
};

// Fetch all uploaded images
export const getImages = () => {
  return axios.get('/api/images');
};

// Delete image by ID
export const deleteImage = (id: number) => {
  return axios.delete(`/api/images/${id}`);
};

// Update image by ID
export const updateImage = (id: number, formData: FormData) => {
  return axios.put(`/api/images/${id}`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
};