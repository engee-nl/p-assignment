# P. Assignmet

This assignment is divided into two project, you have the back end project, which uses Python FastAPI and a front end project which uses Nextjs and React.

## Server architecture

![Server architecture](server-architecture.drawio.png)

## Features

- Upload images in various formats (PNG, BMP, etc.)
- Resize images while maintaining aspect ratio
- Store original images and compressed versions
- Check for existing images using MD5 hash
- Update image dimensions and URLs
- Delete images from the server
- Serve images with a timestamp
- CORS support for cross-origin requests

## Project Structure

```
my_fastapi_project/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── api.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── image.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── image.py
│   ├── utils.py
│   ├── config.py
│   ├── requirements.txt
├── uploaded_images/
├── image_info.json
├── .env
├── Dockerfile
└── README.md
```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/my_fastapi_project.git
   cd my_fastapi_project
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scriptsctivate`
   ```

3. Install the required packages:
   ```bash
   pip install -r app/requirements.txt
   ```

4. Create a `.env` file with your environment variables:
   ```plaintext
   PORT=8000
   ALLOWED_HOSTS=*
   ```

## Running the Application

To run the FastAPI application, use the following command:

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT --reload
```

## API Endpoints

- **Upload Image**: `POST /upload`
- **Get Image**: `GET /image/compressed/{md5}`
- **Update Image Dimensions**: `PUT /images/resize/{md5}`
- **Delete Image**: `DELETE /images/delete/{md5}`
- **Get All Images**: `GET /images/list`

## Example Request to Update Image Dimensions

```javascript
export const updateImageDimensions = async (md5, updateData) => {
  return axios.put(`${API_HOST}/images/resize/${md5}`, updateData, {
    headers: { 'Content-Type': 'application/json' },
  });
};
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License.
