/**
 * NIRMAAN - Camera & Photo Upload Handler
 * Supports multi-angle smartphone photos (Front, Side, Detail, In-Hand) without requiring studio setup.
 */

export const CameraManager = {
  photos: [],

  addPhoto(blob, dataUrl, angle = "Front") {
    const photoObj = {
      id: "p-" + Date.now(),
      blob: blob,
      dataUrl: dataUrl,
      angle: angle,
      timestamp: new Date()
    };
    this.photos.push(photoObj);
    return photoObj;
  },

  getPhotos() {
    return this.photos;
  },

  getPrimaryPhoto() {
    return this.photos.length > 0 ? this.photos[0] : null;
  },

  clearPhotos() {
    this.photos = [];
  },

  createDemoPhotoBlob(craftType = "Pottery") {
    // Creates a realistic canvas craft photo for instant testing
    const canvas = document.createElement("canvas");
    canvas.width = 500;
    canvas.height = 500;
    const ctx = canvas.getContext("2d");

    // Cluttered background (simulating bedsheet / wooden table)
    ctx.fillStyle = "#D7C4B0";
    ctx.fillRect(0, 0, 500, 500);
    ctx.strokeStyle = "#BCA894";
    ctx.lineWidth = 12;
    for (let i = 0; i < 500; i += 60) {
      ctx.beginPath();
      ctx.moveTo(0, i);
      ctx.lineTo(500, i);
      ctx.stroke();
    }

    // Shadow
    ctx.fillStyle = "rgba(40, 30, 20, 0.45)";
    ctx.beginPath();
    ctx.ellipse(250, 390, 140, 35, 0, 0, Math.PI * 2);
    ctx.fill();

    // Handcrafted Item Shape
    if (craftType === "Bamboo") {
      ctx.fillStyle = "#C69C6D";
      ctx.strokeStyle = "#8C6239";
      ctx.lineWidth = 6;
      ctx.beginPath();
      ctx.ellipse(250, 260, 130, 110, 0, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();
    } else if (craftType === "Brass") {
      ctx.fillStyle = "#D4AF37";
      ctx.strokeStyle = "#996515";
      ctx.lineWidth = 5;
      ctx.beginPath();
      ctx.ellipse(250, 270, 120, 100, 0, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();
    } else {
      // Terracotta
      ctx.fillStyle = "#C85A32";
      ctx.strokeStyle = "#8C3415";
      ctx.lineWidth = 6;
      ctx.beginPath();
      ctx.ellipse(250, 270, 130, 105, 0, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();
    }

    return new Promise((resolve) => {
      canvas.toBlob((blob) => {
        resolve({
          blob: blob,
          dataUrl: canvas.toDataURL("image/jpeg", 0.9)
        });
      }, "image/jpeg", 0.9);
    });
  }
};
