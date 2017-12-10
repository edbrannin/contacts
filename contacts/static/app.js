const bus = new Vue();

Vue.component('contacts', {
    props: ['tags'],
    template: `
    <div>
      <h2 v-if="! loading">{{people.length}} People</h2>
      <h2 v-if="loading">Loading...</h2>
      <p v-if="error">{{error}}</p>
      <p v-if="tagList.length">Tags chosen: <span v-for="(tag, index) in tagList"><span v-if="index > 0">, </span>{{tag}}</span></p>
      <div v-if="tagList.length"><button v-on:click="clearTags">Clear Tags</button></div>
      <table class="people" v-if="! loading">
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
      const tags = []
      if (this.tags) {
        tags = this.tags.split(/, */);
      }
      return {
        people: [],
        show_tags: false,
        tagList: tags,
        error: undefined,
        loading: true,
      };
    },
    created: function() {
      this.refresh();
      const self = this;

      bus.$on('tag-selected', function (tag) {
        // Vue.set(this, 'tags', [tag]);
        self.tagList = [tag]
        console.log("Will attempt to show tags: ", self.tagList);
        self.refresh();
      })

    },
    methods: {
        toggleNote: function(index) {
            person = this.people[index];
            // console.log("Person:", person);

            person.show_note = ! person.show_note;
            // console.log("Person:", person);
        },
        refresh: function() {
          this.loading = true;
          console.log('Getting contacts...');
          // GET /someUrl
          this.$http.get('/api/contacts{?tag}', { params: { tag: [ this.tagList ] } }).then(response => {
            console.log("Got contacts:", response, response.body);
            // get body data
            this.people = response.body;
            this.people.forEach(function(item, index, array) {
              Vue.set(item, "show_note", false);
              Vue.set(item, "has_note", Boolean(item.note));
            });
            this.loading = false;
          }, response => {
            console.log("Error getting contacts:", response, response.body);
            this.error = response.body;
          });

      },
      clearTags: function() {
        this.tagList = [];
        this.refresh();
      },
    }
});

Vue.component('contact', {
    props: ['id'],
    template: `
    <div>
      <h2 v-if="person">{{person.name}}</h2>
      <div><button v-if="! editing" v-on:click="edit">Edit</button></div>
      <pre v-if="error">{{error}}</pre>
      <div><button v-on:click="toggleDebug">Debug</button></div>
      <pre v-if="debug">{{JSON.stringify(person, null, 2)}}</pre>
      <table class="person" v-if="person">
        <tbody>
            <tr>
              <th>Name</th>
              <td v-if="editing" class="name"><input v-model="person.name"></input></td>
              <td v-else class="name">{{ person.name }}</td>
          </tr>
          <tr>
              <th>Cell Phone</th>
              <td v-if="editing" class="phone"><input v-model="person.mobile_phone"></input></td>
              <td v-else class="phone">{{person.mobile_phone}}</td>
          </tr>
          <tr>
              <th>Home Phone</th>
              <td v-if="editing" class="phone"><input v-model="person.home_phone"></input></td>
              <td v-else class="phone">{{person.home_phone}}</td>
          </tr>
          <tr>
              <th>Work Phone</th>
              <td v-if="editing" class="phone"><input v-model="person.work_phone"></input></td>
              <td v-else class="phone">{{person.work_phone}}</td>
          </tr>
          <tr>
              <th>e-mail</th>
              <td v-if="editing" class="email"><input v-model="person.email"></input></td>
              <td v-else class="email">{{ person.email }}</td>
          </tr>
          <tr>
              <th>Address</th>
              <td v-if="editing">
                <textarea v-model="person.address"></textarea>
              </td>
              <td v-else>
                <div v-for="note in lines(person.address)">{{note}}</div>
              </td>
          </tr>
          <tr>
              <th>Zip Code</th>
              <td v-if="editing" class="zip"><input v-model="person.zip_code"></input></td>
              <td v-else class="zip">{{ person.zip_code }}</td>
          </tr>

    <!--
    TODO:
    active
    verified_on
    added_on
    created_at
    updated_at
    cached_tag_list
    -->


          <tr>
              <th>Last Name</th>
              <td v-if="editing"><input v-model="person.last_name"></input></td>
              <td v-else>{{ person.last_name }}</td>
          </tr>
          <tr>
              <th>Note</th>
              <td v-if="editing">
                <textarea v-model="person.note"></textarea>
              </td>
              <td v-else>
                <p v-for="note in lines(person.note)">{{note}}</p>
              </td>
          </tr>

          <tr>
              <th>Tags</th>
              <td v-if="editing" class="tags">
                <h3>Active Tags</h3>
                <ul class="tags">
                    <li v-for="tag in person.tags">
                        <a href="#" v-on:click.prevent="removeTag">{{ tag }}</a>
                    </li>
                </ul>
                <hr />
                <h3>Other Tags</h3>
                <ul class="tags">
                    <li v-for="tag in other_tags">
                        <a href="#" v-on:click.prevent="addTag">{{ tag }}</a>
                    </li>
                </ul>
              </td>
              <td v-else class="tags">
                <ul class="tags">
                    <li v-for="tag in person.tags">
                        <a>{{ tag }}</a>
                    </li>
                </ul>
              </td>
          </tr>

        </tbody>
      </table>

      <div v-if="editing">
        <button v-on:click="save">Save</button>
      </div>
    </div>
    `,
    data: function() {
        return {
            person: undefined,
            all_tags: [],
            error: undefined,
            editing: false,
            debug: false,
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

        this.$http.get('/api/tags').then(response => {
            console.log("Got tags:", response, response.body);
            // get body data
            this.all_tags = response.body.map((tag) => { return tag.name; });
        }, response => {
            console.log("Error getting tags:", response, response.body);
            this.error = response.body;
        });
    },
    methods: {
      lines: function(text) {
        return text.split(/\r?\n/);
      },
      edit: function() {
        this.editing = true;
      },
      addTag: function(evt) {
        console.log("ADD tag", evt.srcElement.text);
        this.person.tags.push(evt.srcElement.text);
      },
      removeTag: function(evt) {
        console.log("REMOVE tag", evt.srcElement.text);
        this.person.tags.splice(this.person.tags.indexOf(evt.srcElement.text), 1);
      },
      toggleDebug: function() {
        this.debug = ! this.debug;
      },
      save: function() {
        console.log("PUT %s", '/api/contacts/' + this.id, this.person);
        this.$http.put('/api/contacts/' + this.id, this.person).then(response => {
          this.editing = false;
        }, response => {
          console.log("Error:", response);
        });
      }
    },
  computed: {
    other_tags: (self) => {
      if (self.person === undefined) {
        console.log("self.person is undefined!  self is:", self);
        return [];
      }
      const personTagSet = new Set(self.person.tags);
      const answer = self.all_tags.filter(x => { return ! personTagSet.has(x) });
      console.log("personTagSet", personTagSet);
      console.log("all_tags", self.all_tags);
      console.log("Other tags are:", answer);
      return answer;
    },
  }
});



Vue.component('tags', {
    props: {
      search: String,
      tags: {
        type: Array,
        default: undefined,
      },
    },
    template: `
    <div>
      <h2>{{tags.length}} Tags</h2>
      <p v-if="error">{{error}}</p>
      <ul class="tags">
          <li v-for="tag in tags">
              <a v-bind:href="tag.href" v-on:click.prevent="selectTag">{{ tag.name }}</a>
          </li>
      </ul>
    </div>
    `,
    data: function() {
        return {
            error: undefined
        };
    },
    created: function() {
        // GET /someUrl
        if (this.tags != undefined) {
          return;
        }
        console.log('Getting all tags...');
        this.$http.get('/api/tags').then(response => {
            console.log("Got tags:", response, response.body);
            // get body data
            this.tags = response.body;
        }, response => {
            console.log("Error getting contacts:", response, response.body);
            this.error = response.body;
        });
    },
  methods: {
    selectTag: function(event) {
      console.log(event);
      console.log(event.srcElement.text);
      bus.$emit('tag-selected', event.srcElement.text);
    }
  }

});

