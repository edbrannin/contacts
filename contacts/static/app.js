Vue.component('contacts', {
    props: ['tags'],
    template: `
    <div>
      <h2>{{people.length}} People</h2>
      <p v-if="tags">Tags chosen: {{tags}}</p>
      <table class="people">
        <thead>
          <tr>
            <th>Name</th>
            <th>Phones</th>
            <th>Email</th>
            <th>Zip</th>
            <th>Last Name</th>
            <th>Note</th>
          </tr>
        </thead>
        <tbody>
            <template v-for="(person, index) in people">
            <tr class="person" :key="person.id">
              <td class="name">{{ person.name }}</td>
              <td class="phones">
                  <ul>
                    <li title="Mobile" v-if="person.mobile_phone">C: {{person.mobile_phone}}</li>
                    <li title="Home" v-if="person.home_phone">H: {{person.home_phone}}</li>
                    <li title="Work" v-if="person.work_phone">W: {{person.work_phone}}</li>
                </ul>
              </td>
              <td class="email">{{ person.email }}</td>
              <td class="zip">{{ person.zip_code }}</td>
              <td class="last_name">{{ person.last_name }}</td>
              <td class="show_note" v-if="person.note">
                  <button v-on:click="toggleNote(index)">
                      <span v-if="person.show_note">Hide</span>
                      <span v-else>Show</span>
                  </button>
              </td>
            </tr>

            <tr v-if="person.note && person.show_note" class="person" :key="person.id">
              <td></td>
              <td class="person note" colspan="4">{{person.note}}</td>
            </tr>

            <tr v-if="show_tags" class="person" :key="person.id">
              <td></td>
              <td class="person tags" colspan="4">
                <span class="tag" v-for="tag in person.tags">{{tag}}</span>
              </td>
            </tr>

          </template>
        </tbody>
      </table>
    </div>
    `,
    data: function() {
        return {
            people: [],
            show_tags: false,
            error: undefined,
            sortKey: "last_name"
        };
    },
    created: function() {
        console.log('Getting contacts...');
        // GET /someUrl
        this.$http.get('/api/contacts').then(response => {
            console.log("Got contacts:", response, response.body);
            // get body data
            this.people = response.body;
            this.people.forEach(function(item, index, array) {
                Vue.set(item, "show_note", false);
                Vue.set(item, "has_note", Boolean(item.note));
            });
        }, response => {
            console.log("Error getting contacts:", response, response.body);
            this.error = response.body;
        });
    },
    methods: {
        toggleNote: function(index) {
            person = this.people[index];
            // console.log("Person:", person);

            person.show_note = ! person.show_note;
            // console.log("Person:", person);
        }
    },
    computed: {
        sortedPeople: function() {
            function compare(a, b) {
                const aa = a[this.sortKey];
                const bb = b[this.sortKey];
                if (aa < bb) {
                    return -1;
                } else if (aa > bb) {
                    return 1;
                }
                return 0;
            }

            return this.people.sort(compare);
        }
    }

});
