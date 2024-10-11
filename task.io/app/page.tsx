"use client";

import { useEffect, useState, ChangeEvent } from 'react';
import { uploadImage, getImages, deleteImage, updateImage } from './controllers/imageController';
import Image from 'next/image';

// Define the types for images and API response
interface Image {
  md5: string;
  image_url: string;
}

export default function Home() {
  const [images, setImages] = useState<Image[]>([]);
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);  // For image preview
  const [uploadProgress, setUploadProgress] = useState<number>(0);    // For tracking upload progress
  const [loading, setLoading] = useState<boolean>(false);             // To manage loading 
  const [showModal, setShowModal] = useState<boolean>(false);         // Modal visibility
  const [modalImage, setModalImage] = useState<string | null>(null);  // For the image shown in the modal
  const [notification, setNotification] = useState<{ message: string; errorCode?: string } | null>(null);

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

  const handleImageSelect = (e: ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setSelectedImage(file);
      setPreviewUrl(URL.createObjectURL(file));  // Create a preview URL
    }
  };

  const handleUpload = async () => {
    if (!selectedImage) return;

    const formData = new FormData();
    formData.append('file', selectedImage);

    setLoading(true);  // Start loading

    try {
      await uploadImage(formData, (progressEvent: ProgressEvent) => {
        const progress = Math.round((progressEvent.loaded * 100) / progressEvent.total);
        setUploadProgress(progress);  // Set upload progress
      });
      const response = await getImages();
      setImages(response.data);
      setUploadProgress(0);   // Reset progress after completion
      setSelectedImage(null); // Reset selected image after upload
      setPreviewUrl(null);    // Reset preview after upload
      setNotification(null);  // Clear any previous notification
    } catch (err:any) {
      console.error('Error uploading image:', err);

      // Handle upload error
      const errorMessage = err.response?.data?.detail || 'Upload failed';
      const errorCode = err.response?.status || 'Unknown error';
  
      setNotification({
        message: errorMessage,
        errorCode: errorCode.toString(),
      });
    } finally {
      setLoading(false);  // End loading
    }
  };

  const handleDelete = async (md5: string) => {
    try {
      await deleteImage(md5);
      setImages(images.filter(image => image.md5 !== md5));
    } catch (err) {
      console.error('Error deleting image:', err);
    }
  };

  const handleUpdate = async (md5: string) => {
    if (selectedImage) {
      const formData = new FormData();
      formData.append('image', selectedImage);

      try {
        await updateImage(md5, formData);
        const response = await getImages();
        setImages(response.data);
      } catch (err) {
        console.error('Error updating image:', err);
      }
    }
  };

  const openModal = (originalUrl: string) => {
    setModalImage(originalUrl);  // Set the original image URL
    setShowModal(true);          // Show the modal
  };

  const closeModal = () => {
    setShowModal(false);         // Hide the modal
    setModalImage(null);         // Clear the modal image
  };

  const Notification = ({ message, errorCode }: { message: string; errorCode?: string }) => (
    <div className="fixed top-4 right-4 bg-red-500 text-white p-4 rounded shadow-lg z-50">
      <p>{message}</p>
      {errorCode && <p>Error Code: {errorCode}</p>}
    </div>
  );

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-3xl font-bold text-center mb-8">Image Upload</h1>

      {/* Input for selecting images */}
      <input
        type="file"
        onChange={handleImageSelect}
        className="block w-full mb-4 p-2 border border-gray-300 rounded-md"
      />

      {/* Preview selected image */}
      {previewUrl && (
        <div className="mb-4">
          <h2 className="text-xl font-semibold mb-2">Image Preview:</h2>
          <Image
            src={previewUrl}
            alt="Preview"
            width={500}
            height={500}
            className="w-full h-48 object-cover rounded-md"
          />
        </div>
      )}

      {/* Upload button */}
      {selectedImage && (
        <button
          className="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600"
          onClick={handleUpload}
          disabled={loading}
        >
          {loading ? 'Uploading...' : 'Upload Image'}
        </button>
      )}

      {/* Upload Progress Bar */}
      {loading && (
        <div className="w-full bg-gray-300 rounded-md mt-4">
          <div
            className="bg-blue-500 text-xs font-medium text-white text-center p-1 leading-none rounded-md"
            style={{ width: `${uploadProgress}%` }}
          >
            {uploadProgress}%
          </div>
        </div>
      )}

      {/* Display the list of uploaded images */}
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6 mt-6">
        {images.map((image) => (
          <div
            key={image.md5}
            className="flex flex-col items-center bg-white p-4 rounded-lg shadow-lg"
          >
            <Image
              src={image.image_url}
              alt="Uploaded"
              width={500} // Set appropriate width
              height={500} // Set appropriate height
              className="w-full h-48 object-cover rounded-md mb-4"
            />
            <button
              className="bg-red-500 text-white px-4 py-2 rounded-md mb-2 hover:bg-red-600"
              onClick={() => handleDelete(image.md5)}
            >
              Delete
            </button>
            <button
              className="bg-blue-500 text-white px-4 py-2 rounded-md mb-2 hover:bg-blue-600"
              onClick={() => openModal(image.image_url)}
            >
              View Original
            </button>
            <input
              type="file"
              onChange={handleImageSelect}
              className="block w-full mb-4 p-2 border border-gray-300 rounded-md"
            />
            <button
              className="bg-green-500 text-white px-4 py-2 rounded-md hover:bg-green-600"
              onClick={() => handleUpdate(image.md5)}
            >
              Update
            </button>
          </div>
        ))}
      </div>

    {/* Modal for displaying the original image */}
    {showModal && (
      <div className="fixed inset-0 bg-black bg-opacity-75 flex justify-center items-center z-50">
        <div className="relative bg-white rounded-lg p-6">
          <button
            className="absolute top-2 right-2 text-white bg-red-600 rounded-full w-10 h-10 flex items-center justify-center hover:bg-red-700 focus:outline-none shadow-lg transform translate-x-2 -translate-y-2 transition-all duration-200"
            onClick={closeModal}
            aria-label="Close modal"
          >
            <span className="text-2xl font-bold">&times;</span>
          </button>
          {modalImage && (
            <Image
              src={modalImage}
              alt="Original Image"
              width={800} 
              height={800} 
              className="w-full h-auto max-h-screen object-contain"
            />
          )}
        </div>
      </div>
    )}

    </div>
  );
}