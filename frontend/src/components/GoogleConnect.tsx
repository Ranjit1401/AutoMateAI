"use client";

const API = "http://localhost:8000";

export default function GoogleConnect() {
  const connectGoogle = () => {
    window.location.href = `${API}/google/login`;
  };

  return (
    <button
      onClick={connectGoogle}
      className="rounded-xl bg-blue-600 px-4 py-2 text-white hover:bg-blue-700 transition"
    >
      Connect Google
    </button>
  );
}