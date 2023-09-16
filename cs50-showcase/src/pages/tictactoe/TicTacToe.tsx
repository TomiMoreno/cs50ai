import { useEffect, useMemo, useState } from "react";
import TicTacToeController, { X } from "../../lib/tictactoe";

function TicTacToe({ size = 1 }: { size: number }) {
  const tictactoe = useMemo(() => new TicTacToeController(size), [size]);
  const [gameState, setGameState] = useState(tictactoe.getGameState());
  const { board, status, player, winner } = gameState;

  useEffect(() => {
    setGameState(tictactoe.getGameState());
  }, [tictactoe]);

  const play = (i: number, j: number) => {
    tictactoe.play(i, j);
    setGameState(tictactoe.getGameState());
  };

  const reset = () => {
    tictactoe.reset();
    setGameState(tictactoe.getGameState());
  };

  const isPlaying = status === "playing";

  const currentTurn = isPlaying
    ? `Player ${player}'s turn`
    : winner
    ? `${winner} wins!`
    : "Tie!";
  return (
    <div className="  flex flex-auto flex-col items-center gap-3">
      <h1
        className={`text-4xl ${
          isPlaying
            ? "text-black"
            : winner === X
            ? "text-red-600"
            : "text-blue-600"
        }`}
      >
        {currentTurn}
      </h1>
      <div
        className={`grid justify-items-center content-center gap-4 w-full md:w-[500px] lg:w-[700px]`}
        style={{
          gridTemplateColumns: `repeat(${size}, 1fr)`,
          gridTemplateRows: `repeat(${size}, 1fr)`,
        }}
      >
        {board.map((row, i) =>
          row.map((char, j) => (
            <p
              className={
                "border-2 rounded-lg border-black font-mono text-9xl select-none w-32 h-32 text-center " +
                `${char ? "cursor-not-allowed" : "cursor-pointer"} ${
                  char === "X" ? "text-red-600" : "text-blue-600"
                }`
              }
              onClick={() => !char && play(i, j)}
              key={i * size + j}
            >
              {char}
            </p>
          ))
        )}
      </div>

      <button
        className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
        onClick={reset}
      >
        Reset
      </button>
    </div>
  );
}

export default TicTacToe;
