
import { initializeApp } from "firebase/app";
import { getFirestore } from "firebase/firestore";
import { useState } from "react";
import { collection, addDoc } from "firebase/firestore";
import { db } from "../firebase";


const firebaseConfig = {
  apiKey: "SUA_API_KEY",
  authDomain: "confra-ec-2026.firebaseapp.com",
  projectId: "confra-ec-2026",
  storageBucket: "confra-ec-2026.appspot.com",
  messagingSenderId: "SEU_ID",
  appId: "SEU_APP_ID",
};

const app = initializeApp(firebaseConfig);
export const db = getFirestore(app);

export default function Home() {
  const [name, setName] = useState("");
  const [entered, setEntered] = useState(false);

  async function enterGame() {
    if (!name) return;
    await addDoc(collection(db, "players"), {
      name,
      score: 0,
      totalTime: 0,
      finished: false,
    });
    setEntered(true);
  }

  if (!entered) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-red-700">
        <div className="bg-white p-8 rounded-2xl w-full max-w-md">
          <h1 className="text-3xl font-bold text-center text-red-700">Confra EC 2026</h1>
          <input
            className="w-full border p-3 mt-6 rounded-xl"
            placeholder="Digite seu nome"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
          <button
            onClick={enterGame}
            className="w-full bg-red-700 text-white p-3 rounded-xl mt-4"
          >
            Entrar
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-red-700 text-white">
      <h2 className="text-2xl font-bold">Aguardando início pelo apresentador</h2>
    </div>
  );
}

// ================= pages/admin-ec2026.jsx =================
import { useEffect, useState } from "react";
import { collection, getDocs, updateDoc, doc } from "firebase/firestore";
import { db } from "../firebase";

export default function Admin() {
  const [players, setPlayers] = useState([]);

  async function loadPlayers() {
    const snap = await getDocs(collection(db, "players"));
    setPlayers(snap.docs.map(d => ({ id: d.id, ...d.data() })));
  }

  useEffect(() => { loadPlayers(); }, []);

  return (
    <div className="min-h-screen bg-black text-white p-10">
      <h1 className="text-3xl font-bold mb-6">Painel do Apresentador</h1>
      <button onClick={loadPlayers} className="bg-green-600 px-4 py-2 rounded-xl">Atualizar jogadores</button>

      <div className="mt-6">
        {players.map(p => (
          <div key={p.id} className="flex justify-between border-b py-2">
            <span>{p.name}</span>
            <span>{p.score} pts</span>
          </div>
        ))}
      </div>
    </div>
  );
}

// ================= REGRAS =================
// - Tempo fixo: 30s por pergunta
// - Ranking: score DESC, totalTime ASC
// - Ranking exibido apenas no final
// - Perguntas devem ser salvas no Firestore: collection 'questions'
