"use client";

import { useEffect, useState, ChangeEvent } from 'react';
import { uploadImage, getImages, deleteImage, updateImage } from './services/imageService';

// Define the types for images and API response
interface Image {
  id: number;
  url: string;
}

export default function Home() {
  const [images, setImages] = useState<Image[]>([]);
  const [selectedImage, setSelectedImage] = useState<File | null>(null);

  useEffect(() => {
    const fetchImages = async () => {
      try {
        const response = await getImages();
        setImages(response.data);
      } catch (error) {
        console.error('Error fetching images:', error);
      }
    };
    fetchImages();
  }, []);

  const handleUpload = async (e: ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];

    if (file) {
      const formData = new FormData();
      formData.append('image', file);

      try {
        await uploadImage(formData);
        const response = await getImages();
        setImages(response.data);
      } catch (err) {
        console.error('Error uploading image:', err);
      }
    }
  };

  const handleDelete = async (id: number) => {
    try {
      await deleteImage(id);
      setImages(images.filter(image => image.id !== id));
    } catch (err) {
      console.error('Error deleting image:', err);
    }
  };

  const handleUpdate = async (id: number) => {
    if (selectedImage) {
      const formData = new FormData();
      formData.append('image', selectedImage);

      try {
        await updateImage(id, formData);
        const response = await getImages();
        setImages(response.data);
      } catch (err) {
        console.error('Error updating image:', err);
      }
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-3xl font-bold text-center mb-8">Image Upload</h1>

      {/* Input for uploading images */}
      <input
        type="file"
        onChange={handleUpload}
        className="block w-full mb-4 p-2 border border-gray-300 rounded-md"
      />

      {/* Display the list of uploaded images */}
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
        {images.map((image) => (
          <div
            key={image.id}
            className="flex flex-col items-center bg-white p-4 rounded-lg shadow-lg"
          >
            <img
              src={image.url}
              alt="Uploaded"
              className="w-full h-48 object-cover rounded-md mb-4"
            />
            <button
              className="bg-red-500 text-white px-4 py-2 rounded-md mb-2 hover:bg-red-600"
              onClick={() => handleDelete(image.id)}
            >
              Delete
            </button>
            <input
              type="file"
              onChange={(e: ChangeEvent<HTMLInputElement>) => setSelectedImage(e.target.files?.[0] || null)}
              className="block w-full mb-4 p-2 border border-gray-300 rounded-md"
            />
            <button
              className="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600"
              onClick={() => handleUpdate(image.id)}
            >
              Update
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}