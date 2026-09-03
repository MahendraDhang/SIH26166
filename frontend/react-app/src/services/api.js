const API_URL = "https://sih26166.onrender.com";

export async function uploadImages(image1, image2) {
  const formData = new FormData();

  formData.append("image1", image1);
  formData.append("image2", image2);

  const response = await fetch(
    `${API_URL}/api/analysis/upload`,
    {
      method: "POST",
      body: formData,
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail || `Upload failed (${response.status})`
    );
  }

  return data;
}