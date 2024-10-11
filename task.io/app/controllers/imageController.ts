import axios from 'axios';

const API_HOST = process.env.NEXT_PUBLIC_API_HOST;

// Upload image with progress bar
export const uploadImage = (formData: FormData, onUploadProgress: (progressEvent: ProgressEvent) => void) => {
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();

    xhr.open('POST', `${API_HOST}/upload`, true);

    // Set up event listener for progress
    xhr.upload.onprogress = onUploadProgress;

    xhr.onload = () => {
      if (xhr.status >= 200 && xhr.status < 300) {
        resolve(JSON.parse(xhr.responseText));
      } else {
        reject(JSON.parse(xhr.responseText))
        //reject(new Error('Failed to upload image'));
      }
    };

    xhr.onerror = () => {
      reject(new Error('Network error'));
    };

    xhr.send(formData);
  });
};

// Upload image
/*
export const uploadImage = async (formData: FormData) => {
  return await axios.post(`${API_HOST}/upload`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
};
*/

// Get images
export const getImages = async () => {
  return await axios.get(`${API_HOST}/images`);
};

// Delete image
export const deleteImage = async (md5: string) => {
  return await axios.delete(`${API_HOST}/delete/${md5}`);
};

// Update image
export const updateImage = async (md5: string, formData: FormData) => {
  return await axios.put(`${API_HOST}/images/${md5}`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
};