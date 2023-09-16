import { useState } from "react";
import TicTacToeController from "./pages/tictactoe/TicTacToe";

function App() {
  const [size, setSize] = useState(2);

  const plusOne = () => setSize(size + 1);
  const minusOne = () => setSize(Math.max(0, size - 1));

  return (
    <div className="flex flex-col items-center gap-3">
      <div className="flex flex-row items-center">
        <button
          className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
          onClick={minusOne}
        >
          -
        </button>
        <h1 className="text-4xl mx-3">{size}</h1>
        <button
          className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
          onClick={plusOne}
        >
          +
        </button>
      </div>
      <TicTacToeController size={size} />
    </div>
  );
}

export default App;
