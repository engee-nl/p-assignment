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
    <div className="fixed inset-0 z-50 items-center justify-center bg-black bg-opacity-75 overflow-y-auto">
      <div className="relative max-w-full p-8 bg-white rounded-lg shadow-lg" style={{ margin: '3rem' }} >
        {/* Close Button */}
        <button
            className="absolute top-[-14px] right-[-14px] top-2 right-2 text-white bg-red-600 rounded-full w-10 h-10 flex items-center justify-center hover:bg-red-700 focus:outline-none shadow-lg transform translate-x-2 -translate-y-2 transition-all duration-200"
            onClick={onClose}
            aria-label="Close modal"
        >
            <span className="text-2xl font-bold">&times;</span> {/* Using a larger × symbol */}
        </button>

        {/* Image Preview */}
        <div className="p-4">
          <h2 className="text-xl font-semibold mb-2">Original Image:</h2>
          <Image
            src={originalImageUrl}
            alt="Original"
            width={undefined} // Adjust width based on fullscreen
            height={undefined} // Adjust height based on fullscreen
            className={'object-cover'}
          />
        </div>
      </div>
    </div>
  );
};

export default Modal;