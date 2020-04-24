import React,  { useState } , {Component} from 'react';

class App extends Component {
  render() {
    const [userQUery, setUserQuery] = useState();
    const updateuserQUery = (event) =>{
      console.log('userQuery', userQUery)
      setUserQuery(event.target.value);
    }
    return (
      <div className="App">
        <input value={userQUery} onChange={updateuserQUery}/>
        <button>Search</button>

        App
      </div>
    );
  }
}

export default App;
