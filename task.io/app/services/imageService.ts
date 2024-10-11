import axios from 'axios';

const API_HOST = process.env.NEXT_PUBLIC_API_HOST;

// Upload image
export const uploadImage = async (formData: FormData) => {
  return await axios.post(`${API_HOST}/upload`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
};

// Get images
export const getImages = async () => {
  return await axios.get(`${API_HOST}/images`);
};

// Delete image
export const deleteImage = async (id: number) => {
  return await axios.delete(`${API_HOST}/delete/${id}`);
};

// Update image
export const updateImage = async (id: number, formData: FormData) => {
  return await axios.put(`${API_HOST}/images/${id}`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
};