// components/Modal.tsx
import React from 'react';
import Image from 'next/image';

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  originalImageUrl: string;
}

const Modal: React.FC<ModalProps> = ({ isOpen, onClose, originalImageUrl }) => {

  if (!isOpen) return null; // Don't render the modal if it's not open

  return (
    <div
      className={`fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center transition-all duration-300 z-50`}
    >
      <div
        className={`relative bg-white rounded-lg overflow-hidden w-full h-full`}
      >
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-[-14px] right-[-14px] bg-gray-200 rounded-full p-1 shadow-md hover:bg-gray-300 focus:outline-none"
          aria-label="Close"
        >
          <span className="text-lg">×</span>
        </button>

        {/* Image Preview */}
        <div className="p-4">
          <h2 className="text-xl font-semibold mb-2">Original Image:</h2>
          <Image
            src={originalImageUrl}
            alt="Original"
            width={undefined} // Adjust width based on fullscreen
            height={undefined} // Adjust height based on fullscreen
            className={'w-full h-full object-cover'}
          />
        </div>
      </div>
    </div>
  );
};

export default Modal;