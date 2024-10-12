"use client";

import { useEffect, useState, useRef, ChangeEvent } from 'react';
import { uploadImage, getImages, deleteImage, updateImageDimensions } from './controllers/imageController';
import Image from 'next/image';
import Modal from './components/Modal';
import Notification from './components/Notification';
import { AxiosResponse } from 'axios';
import { CustomError, ImageResponse } from './types/responseTypes'
import { ImageType } from './types/imageTypes'
import ExpandIcon from './components/ExpandIcon';

export default function Home() {
  const [images, setImages] = useState<ImageType[]>([]);
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);  // For image preview
  const [uploadProgress, setUploadProgress] = useState<number>(0);    // For tracking upload progress
  const [loading, setLoading] = useState<boolean>(false);             // To manage loading 
  const [showModal, setShowModal] = useState<boolean>(false);         // Modal visibility
  const [modalImage, setModalImage] = useState<string>("");           // For the image shown in the modal
  const [notification, setNotification] = useState<{ message: string; errorCode?: string } | null>(null);

  const [imageDimensions, setImageDimensions] = useState<{ [key: string]: { width: number; height: number } }>({});

  const fileInputRef = useRef<HTMLInputElement | null>(null);

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

      // Clear the file input field after successful upload
      if (fileInputRef.current) {
        fileInputRef.current.value = '';  // Reset the input field
      }
    } catch (err: unknown) {

      // Use type assertion to cast the unknown error to CustomError
      const customError = err as CustomError;

      const errorMessage = customError?.detail || 'Upload failed'; // Accessing the message
      const errorCode = customError?.status || 'Unknown error'; // Accessing the status code

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
      const response: AxiosResponse<ImageResponse> = await deleteImage(md5);
      if (response && response.data.message) {
        setNotification({
          message: response.data.message,
          errorCode: "",
        });
      }

      // Clear the file input field after successful upload
      if (fileInputRef.current) {
        fileInputRef.current.value = '';  // Reset the input field
      }

      setImages(images.filter(image => image.md5 !== md5));
    } catch (err) {
      console.error('Error deleting image:', err);
      setNotification(null);
    }
  };

  const handleDimensionChange = (md5: string, dimension: 'width' | 'height', value: number) => {
    setImageDimensions((prev) => ({
      ...prev,
      [md5]: {
        ...prev[md5],
        [dimension]: value,
      },
    }));
  };

  const handleUpdate = async (md5: string) => {
    const dimensions = imageDimensions[md5];
    const postData = { width: dimensions.width, height: dimensions.height }

    try {
      const response_update: AxiosResponse<ImageResponse> = await updateImageDimensions(md5, postData);
      if (response_update && response_update.data.message) {
        setNotification({
          message: response_update.data.message,
          errorCode: "",
        });
      }

      const response = await getImages();
      setImages(response.data);

      handleDimensionChange(md5, 'width', 0);
      handleDimensionChange(md5, 'height', 0);
    } catch (err) {
      console.error('Error updating image:', err);
    }
  };

  const openModal = (originalUrl: string) => {
    setModalImage(originalUrl);  // Set the original image URL
    setShowModal(true);          // Show the modal
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      {notification && (
        <Notification message={notification.message} error={notification.errorCode} />
      )}
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
            className="flex flex-col items-center bg-white p-4 rounded-lg shadow-lg relative"
          >
            <Image
              src={image.image_url}
              alt="Uploaded"
              width={500} // Set appropriate width
              height={500} // Set appropriate height
              className="w-full h-48 object-cover rounded-md mb-4"
            />
            <button
              onClick={() => openModal(image.image_url)}
              className="absolute top-[24px] right-[24px] top-2 right-2 bg-gray-800 bg-opacity-50 text-white rounded-full p-1 hover:bg-opacity-75 focus:outline-none"
              aria-label="Expand Image"
            >
              <ExpandIcon /> 
            </button>

            <button
              className="bg-red-500 text-white rounded-md w-full px-4 py-2 hover:bg-red-600"
              onClick={() => handleDelete(image.md5)}
            >
              Delete
            </button>

            <div className="h-[14px] bg-white-500"></div>

            <button
              className="bg-blue-500 text-white rounded-md w-full px-4 py-2 hover:bg-blue-600"
              onClick={() => openModal(image.original_image_url)}
            >
              View Original
            </button>

            <div className="h-[14px] bg-white-500"></div>

            <div className="flex space-x-2">
              <input
                type="number"
                placeholder="Width"
                value={imageDimensions[image.md5]?.width > 0 ? imageDimensions[image.md5]?.width : ''}
                onChange={(e) => handleDimensionChange(image.md5, 'width', Number(e.target.value))}
                className="border rounded p-2 w-full sm:w-1/2"
              />
              <input
                type="number"
                placeholder="Height"
                value={imageDimensions[image.md5]?.height > 0 ? imageDimensions[image.md5]?.height : ''}
                onChange={(e) => handleDimensionChange(image.md5, 'height', Number(e.target.value))}
                className="border rounded p-2 w-full sm:w-1/2"
              />
            </div>

            <button
              onClick={() => handleUpdate(image.md5)}
              className="mt-2 bg-green-500 text-white rounded p-2 w-full hover:bg-green-600"
            >
              Update dimension
            </button>

          </div>
        ))}
      </div>

      <Modal
        isOpen={showModal}
        onClose={() => setShowModal(false)}
        originalImageUrl={modalImage}
      />

    </div>
  );
}