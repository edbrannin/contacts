Vue.component('contacts', {
    props: ['tags'],
    template: `
    <div>
      <h2>{{people.length}} People</h2>
      <p v-if="tags">Tags chosen: {{tags}}</p>
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Phones</th>
            <th>Email</th>
            <th>Note</th>
            <th>Zip</th>
            <th>Last Name</th>
          </tr>
        </thead>
        <tbody>
            <template v-for="person in people">
            <tr class="person">
              <td class="name">{{ person.name }}</td>
              <td class="phones">{{ person.phones }}</td>
              <td class="email">{{ person.email }}</td>
              <td class="zip">{{ person.zip }}</td>
              <td class="last_name">{{ person.last_name }}</td>
              <td class="show_note"><button text="Show Note"></button>
            </tr>
            <tr v-if="person.note and person.show_note">
              <td class="person note" colspan="5">{{person.note}}
            </tr>
          </template>
        </tbody>
      </table>
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
