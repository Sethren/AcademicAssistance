import React from "react";

class App extends React.Component {
  state = {
    name: '',
  };
  constructor(props) {
    super(props); 
  }
  render() {
    return (
      <div>
        <label>Name: </label>
        <input
          type="text"
          value={this.state.name}
          onInput={(event) => this.handleInput(event)}
        />
        <h1>Hello {this.state.name}!</h1>
      </div>
    );
  }
  handleInput = (event) => {
    this.setState({ name: event.target.value });
  }
}

export default App;