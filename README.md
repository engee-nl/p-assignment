# P. Assignment

This assignment consists of two separate projects: a back-end project built with Python FastAPI and a front-end project developed using Next.js and React. To simplify sharing, both projects have been combined into a single repository. However, following best practices, each project should ideally be stored in its own separate repository.
A demo section is included at the end of this README. Check out the URL and try the demo.

## Server architecture

If I had access to the necessary servers and time, I would set up the architecture as outlined below. This design is based on the following considerations:

- **Zero downtime**: If the server's operating system needs an update, the load balancer can be adjusted to redirect traffic, ensuring continuous availability.
- **Faster image download speeds and caching**: By leveraging AWS S3 and CloudFront (with global distribution), we can significantly improve performance.
- **Traffic distribution**: Using a load balancer, along with multiple Docker containers and servers, helps evenly distribute traffic and optimize resource utilization. Additionally, by implementing a master-slave database configuration, we can optimize database performance. The master database handles write operations, while the slave(s) handle read operations, reducing the load on the master and improving overall efficiency for read-heavy applications.

Currently, both projects are implemented on a single server because I don't have separate servers and a dedicated database available.

![Server architecture](server-architecture.drawio.png)

# Back-end

The back-end of this project is built using Python's FastAPI framework. It handles core functionalities such as image uploads, compression, resizing, and file management. Uploaded images are processed to ensure optimal quality and storage efficiency, and the application interacts with local file storage. The back-end also supports API endpoints for image retrieval, deletion, and updating image dimensions. Additionally, it ensures the integrity of image data through MD5 hashing.

## Features

- Upload images in various formats (PNG, BMP, etc.)
- Resize images while maintaining aspect ratio
- Store original images and compressed versions
- Check for existing images using MD5 hash
- Update image dimensions
- Delete images from the server
- Serve images with a timestamp
- CORS support for cross-origin requests

## Project Structure

```
api.task.io.image/
├── app/
│   ├── controllers/
│   │   ├── __init__.py
│   │   ├── image_controller.py
│   │   └── local_image_controller.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   └── image_schema.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── image_service.py
│   │   └── local_image_service.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── file_utils.py
│   │   └── s3_utils.py
│   ├── __init__.py
│   ├── config.py
│   └── main.py
├── logs/
│   └── app.log
├── uploaded_images/
├── image_list.json
├── .env
├── Dockerfile
├── README.md
└── requirements.txt
```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/engee-nl/p-assignment.git
   cd api.task.io.image
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. Install the required packages:
   ```bash
   pip install -r app/requirements.txt
   ```

4. Create a `.env` file with your environment variables:
   ```plaintext
    AWS_ACCESS_KEY_ID=your-access-key
    AWS_SECRET_ACCESS_KEY=your-secret-key
    S3_BUCKET_NAME=your-bucket-name

    DATABASE_URL=mysql+pymysql://username:password@localhost/dbname

    IMAGE_HOST_URL=http://ec2-43-201-64-153.ap-northeast-2.compute.amazonaws.com:8001
   ```

## Running the Application

To run the FastAPI application, use the following command:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload --timeout-keep-alive 180
```

## API Endpoints

- **Upload Image**: `POST /image/upload`
- **Get Image**: `GET /image/get/compressed/{md5}`
- **Get Original Image**: `GET /image/get/original/{md5}`
- **Update Image Dimensions**: `PUT /image/resize/{md5}`
- **Delete Image**: `DELETE /image/delete/{md5}`
- **Get All Images**: `GET /image/list`

## Example Request to Update Image Dimensions

```javascript
export const updateImageDimensions = async (md5, updateData) => {
  return axios.put(`${API_HOST}/image/resize/${md5}`, updateData, {
    headers: { 'Content-Type': 'application/json' },
  });
};
```

## Technologies Used

- **Python**: 3.8 or higher
- **FastAPI**: For building the web API
- **Pydantic**: For data validation and settings management
- **Uvicorn**: ASGI server for running the application
- **Pillow**: For image processing
- **JSON**: For storing image metadata

# Front-end

This project is a simple image upload and management application using **Next.js** with **TypeScript** and **Tailwind CSS**. It allows users to:
1. Upload images to the server.
2. View a list of uploaded images.
3. Delete and update image dimensions.
4. Preview the original and compressed images in a modal.

The frontend communicates with a backend API to manage the images. The server processes images and stores them.

## Features

- **Image Upload with Progress Bar**: Upload images with a visible progress bar showing the percentage of upload completion.
- **Preview Images Before Upload**: Users can preview the uncompressed image before uploading it.
- **View, Delete, and Update**: Users can view original images in a modal, delete images, and update their dimensions (width/height).
- **Tailwind CSS for Styling**: The UI is styled with Tailwind CSS for a modern and responsive design.

## Project Structure

```bash
task.io/
├── app/
│   ├── api/
│   ├── components/
│   │   ├── ExpandIcon.tsx        # Icon component for the expand (view original) button.
│   │   ├── Modal.tsx             # Modal for showing full-screen images.
│   │   └── Notification.tsx      # Notification component for success and error messages.
│   ├── controllers/
│   │   └── imageController.ts    # Controller and Axios services for interacting with the backend API.
│   ├── fonts/
│   │   ├── GeistMonoVF.woff
│   │   └── GeistVF.woff
│   ├── types/
│   │   ├── imageTypes.ts
│   │   └── responseTypes.ts
│   ├── favicon.ico
│   ├── globals.css
│   ├── layout.tsx
│   └── page.tsx
├── public/                       # Static files
├── image_list.json
├── .env.local                    # Local environment variables (API host, etc.).
├── .env.production               # Production environment variables (API host, etc.).
├── .eslintrc.json
├── .gitignore
├── next.config.mjs
├── package.json
├── postcss.config.mjs
├── README.md
├── tailwind.config.ts
└── tsconfig.json
```

## How to Run the Project

### Prerequisites

- Node.js
- npm or yarn package manager

### Installation Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/engee-nl/p-assignment.git
   cd task.io
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Set up environment variables:
   Create a `.env` file in the root directory and add the API host.
   ```
   NEXT_PUBLIC_API_HOST=http://ec2-43-201-64-153.ap-northeast-2.compute.amazonaws.com:8001
   ```

4. Run the development server:
   ```bash
   npm run dev
   ```

5. Open your browser and navigate to:
   ```
   http://localhost:3000
   ```

## Usage

### Uploading Images

1. Click the "Choose File" button to select an image.
2. Preview the image before uploading.
3. Click the "Upload" button to upload the image.
4. A progress bar will indicate the upload progress.

### Viewing Images

- Uploaded images are displayed in a list.
- To view the original image, click the expand icon on the image to open it in a full-screen modal.

### Deleting and Updating Images

- To delete an image, click the "Delete" button next to the image.
- To resize the image, input the desired dimensions (width/height) and click "Update."

## Technologies Used

- **Next.js**: React framework for building server-side rendered applications.
- **TypeScript**: Strongly-typed JavaScript for better code quality and maintainability.
- **Tailwind CSS**: Utility-first CSS framework for building responsive and modern UIs.
- **Axios**: For making HTTP requests to the backend API.
- **React Hooks**: For managing state and lifecycle methods in functional components.

# Demo

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License.
