export const X = "X";
export const O = "O";
export const EMPTY = null;

const PLAYING = "playing";

export type Player = typeof X | typeof O | typeof EMPTY;
export type Board = Player[][];
export type status = typeof PLAYING | Player;

export default class TicTacToe {
  private board: Board;
  private player: Player;
  private status: status;

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

  // We asume there's only one winner
  checkWinner = (board: Board): Player => {
    let possibleWinner: Player = board[0][0];

    // Check diagonal
    for (let i = 0; i < board.length; i++) {
      if (board[i][i] !== possibleWinner) {
        possibleWinner = EMPTY;
        break;
      }
    }
    if (possibleWinner) return possibleWinner;

    possibleWinner = board[0][board.length - 1];
    for (let i = 0; i < board.length; i++) {
      if (board[i][board.length - 1 - i] !== possibleWinner) {
        possibleWinner = EMPTY;
        break;
      }
    }

    if (possibleWinner) return possibleWinner;
    // Check rows
    for (let i = 0; i < board.length; i++) {
      possibleWinner = board[i][0];
      for (let j = 0; j < board[i].length; j++) {
        if (board[i][j] !== possibleWinner) {
          possibleWinner = EMPTY;
          break;
        }
      }
      if (possibleWinner) {
        return possibleWinner;
      }
    }

    // Check columns
    for (let i = 0; i < board.length; i++) {
      possibleWinner = board[0][i];
      for (let j = 0; j < board[i].length; j++) {
        if (board[j][i] !== possibleWinner) {
          possibleWinner = EMPTY;
          break;
        }
      }
      if (possibleWinner) {
        return possibleWinner;
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

    if (winner) {
      this.status = winner;
    } else {
      this.player = this.player === X ? O : X;
    }
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
