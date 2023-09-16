export const X = "X";
export const O = "O";
export const EMPTY = null;

export const PLAYING = "playing";
export const TIE = "tie";

export type Player = typeof X | typeof O | typeof EMPTY;
export type Board = Player[][];
export type Status = typeof PLAYING | typeof TIE | Player;
export type Winner = {
  player: Player;
  from: { row: number; column: number };
  to: { row: number; column: number };
};

export default class TicTacToe {
  private board: Board;
  private player: Player;
  private status: Status;
  private winner?: Winner;

  constructor(size: number) {
    console.log("Creating board of size: ", size);
    this.board = this.createBoard(size);
    this.player = X;
    this.status = PLAYING;
  }

  createBoard = (size: number) => {
    const board: Player[][] = [];
    for (let i = 0; i < size; i++) {
      const row: Player[] = [];
      for (let j = 0; j < size; j++) {
        row.push(EMPTY);
      }
      board.push(row);
    }

    return board;
  };

  // This is a helper function to check lines for a winner
  private checkLine = (line: Player[]): Player => {
    const possibleWinner = line[0];
    for (const cell of line) {
      if (cell !== possibleWinner) {
        return EMPTY;
      }
    }
    return possibleWinner;
  };

  // Use it in your checkWinner function
  checkWinner = (board: Board): Player => {
    // Diagonals, Rows and Columns checks simplified
    const diagonalsAndLines = [
      // Diagonals
      board.map((_, i) => board[i][i]),
      board.map((_, i) => board[i][board.length - i - 1]),
      // Rows
      ...board,
      // Columns
      ...board[0].map((_, i) => board.map((row) => row[i])),
    ];

    for (const line of diagonalsAndLines) {
      const winner = this.checkLine(line);
      if (winner !== EMPTY) {
        return winner;
      }
    }

    return EMPTY;
  };

  copyBoard = (board: Board) => {
    const boardCopy: Board = [];
    for (let i = 0; i < board.length; i++) {
      const row: Player[] = [];
      for (let j = 0; j < board[i].length; j++) {
        row.push(board[i][j]);
      }
      board.push(row);
    }

    return boardCopy;
  };

  getGameState = () => ({
    board: this.board,
    player: this.player,
    status: this.status,
    winner: this.checkWinner(this.board),
  });

  play = (row: number, column: number) => {
    if (this.status !== PLAYING) return;

    if (this.board[row][column] !== EMPTY) return;

    this.board[row][column] = this.player;

    const winner = this.checkWinner(this.board);
    const isBoardFull = this.isBoardFull();

    if (winner || isBoardFull) {
      this.status = winner || TIE;
    } else {
      this.player = this.player === X ? O : X;
    }
  };

  isBoardFull = () => {
    for (const row of this.board) {
      for (const cell of row) {
        if (cell === EMPTY) {
          return false;
        }
      }
    }
    return true;
  };

  reset = () => {
    this.board = this.createBoard(this.board.length);
    this.player = X;
    this.status = PLAYING;
  };

  private logBoard = () => {
    console.log("Board: " + this.player + " turn ", this.status);
    for (let i = 0; i < this.board.length; i++) {
      console.log(this.board[i]);
    }
  };
}
