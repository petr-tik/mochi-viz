import React from 'react';
import './App.css';
import Form from './Form';
import Graph from './Graph';
import Charts from './Charts';

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      cards: [],
      links: [],
      loading: false,
      error: false,
      view: 'graph',
    };
  }

  // Helper function to filter orphan cards
  filterOrphanCards = (cards, links) => {
    const linkedCardIds = new Set(
      links.flatMap(link => [link.source, link.target])
    );
    return cards.filter(card => linkedCardIds.has(card.id));
  };

  getCards = event => {
    event.preventDefault();
    this.setState({ loading: true, cards: [], links: [], error: false });
    const formData = new FormData();
    formData.append('api_key', event.currentTarget.elements.apiKey.value);

    fetch('/api/cards', {
      method: 'POST',
      body: formData,
    })
      .then(response => response.json())
      .then(data => {
        const { cards, links, error } = data;

        // Filter out orphan cards
        const filteredCards = this.filterOrphanCards(cards, links);

        this.setState({ cards: filteredCards, links, loading: false, error });
      })
      .catch(() => this.setState({ loading: false, error: true }));
  };

  setView = view => {
    this.setState({ view });
  };

  render() {
    return (
      <div className="App">
        <Form
          getCards={this.getCards}
          setView={this.setView}
          cards={this.state.cards}
          loading={this.state.loading}
          error={this.state.error}
        />
        <div style={{ display: this.state.view === 'graph' ? 'block' : 'none' }}>
          <Graph
            cards={this.state.cards}
            links={this.state.links}
            loading={this.state.loading}
          />
        </div>
        <div style={{ display: this.state.view === 'charts' ? 'block' : 'none' }}>
          <Charts cards={this.state.cards} />
        </div>
      </div>
    );
  }
}

export default App;
