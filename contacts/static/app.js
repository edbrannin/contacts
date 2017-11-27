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
              <td class="name">
                  <a v-bind:href="person.href">{{ person.name }}</a>
              </td>
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
    }
});

Vue.component('contact', {
    props: ['id'],
    template: `
    <div>
      <h2 v-if="person">{{person.name}}</h2>
      <p v-if="error">{{error}}</p>
      <table class="person" v-if="person">
        <tbody>
            <tr>
              <th>Name</th>
              <td class="name">
                  <a v-bind:href="person.href">{{ person.name }}</a>
              </td>
          </tr>
          <tr>
              <th>Phones</th>
              <td class="phones">
                  <ul>
                    <li title="Mobile" v-if="person.mobile_phone">C: {{person.mobile_phone}}</li>
                    <li title="Home" v-if="person.home_phone">H: {{person.home_phone}}</li>
                    <li title="Work" v-if="person.work_phone">W: {{person.work_phone}}</li>
                </ul>
              </td>
          </tr>
          <tr>
              <th>e-mail</th>
              <td class="email">{{ person.email }}</td>
          </tr>
          <tr>
              <th>Address</th>
              <div v-for="note in lines(person.address)">{{note}}</div>
          </tr>
          <tr>
              <th>Zip Code</th>
              <td class="zip">{{ person.zip_code }}</td>
          </tr>
          <tr>
              <th>Last Name</th>
              <td>{{ person.last_name }}</td>
          </tr>
          <tr>
              <th>Note</th>
              <td>
                <p v-for="note in lines(person.note)">{{note}}</p>
              </td>
          </tr>

        </tbody>
      </table>
    </div>
    `,
    data: function() {
        return {
            person: undefined,
            error: undefined
        };
    },
    created: function() {
        console.log('Getting contacts...');
        // GET /someUrl
        this.$http.get('/api/contacts/' + this.id).then(response => {
            console.log("Got contact:", response, response.body);
            // get body data
            this.person = response.body;
        }, response => {
            console.log("Error getting contacts:", response, response.body);
            this.error = response.body;
        });
    },
    methods: {
        lines: function(text) {
            return text.split(/\r?\n/);
        }
    }
});



Vue.component('tags', {
    props: ['search'],
    template: `
    <div>
      <h2>{{tags.length}} Tags</h2>
      <p v-if="error">{{error}}</p>
      <ul class="tags">
          <li v-for="tag in tags">
              <a v-bind:href="tag.href">{{tag.name}}</a>
          </li>
      </ul>
    </div>
    `,
    data: function() {
        return {
            tags: [],
            error: undefined
        };
    },
    created: function() {
        console.log('Getting contacts...');
        // GET /someUrl
        this.$http.get('/api/tags').then(response => {
            console.log("Got tags:", response, response.body);
            // get body data
            this.tags = response.body;
        }, response => {
            console.log("Error getting contacts:", response, response.body);
            this.error = response.body;
        });
    }
});

