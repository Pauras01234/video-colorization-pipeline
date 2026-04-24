import { useState } from "react";

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [jobId, setJobId] = useState<string | null>(null);
  const [status, setStatus] = useState<string>("idle");
  const [videoUrl, setVideoUrl] = useState<string | null>(null);

  const upload = async () => {
    if (!file) {
      alert("Select a video first");
      return;
    }

    setStatus("uploading");
    setVideoUrl(null);

    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch("http://127.0.0.1:8000/upload", {
      method: "POST",
      body: formData,
    });

    const data = await res.json();

    setJobId(data.job_id);
    setStatus("queued");

    pollStatus(data.job_id);
  };

  const pollStatus = (jobId: string) => {
    const interval = setInterval(async () => {
      const res = await fetch(`http://127.0.0.1:8000/status/${jobId}`);
      const data = await res.json();

      setStatus(data.status);

      if (data.status === "finished") {
        clearInterval(interval);
        setVideoUrl(`http://127.0.0.1:8000/download/${jobId}`);
      }

      if (data.status === "failed") {
        clearInterval(interval);
        alert("Processing failed");
      }
    }, 3000);
  };

  return (
    <div style={{ padding: 40, fontFamily: "Arial" }}>
      <h1>Video Colorizer</h1>

      <input
        type="file"
        accept="video/*"
        onChange={(e) => setFile(e.target.files?.[0] || null)}
      />

      <br />
      <br />

      <button onClick={upload}>
        Upload
      </button>

      <p>Status: {status}</p>

      {jobId && <p>Job ID: {jobId}</p>}

      {videoUrl && (
        <>
          <h2>Result</h2>
          <video src={videoUrl} controls width="700" />
          <br />
          <a href={videoUrl} download>
            Download video
          </a>
        </>
      )}
    </div>
  );
}

export default App;