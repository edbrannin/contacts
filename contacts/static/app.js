Vue.component('contacts', {
    props: ['tags'],
    template: `
    <div>
    <p v-if="tags">Tags chosen: {{tags}}</p>
    <ul>
        <li v-for="person in people">{{ person.name }}</li>
    </ul>
    </div>
    `,
    data: function() {
        return {
            people: [],
            error: undefined
        };
    },
    created: function() {
        console.log('Getting contacts...');
        // GET /someUrl
        this.$http.get('/api/contacts').then(response => {
            console.log("Got contacts:", response, response.body);
            // get body data
            this.people = response.body;
        }, response => {
            console.log("Error getting contacts:", response, response.body);
            this.error = response.body;
        });
    }
});
