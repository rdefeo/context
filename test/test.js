var 
  assert = require("assert"),
  session = require("../lib/session")

describe('session', function(){
  describe('newestUnique', function(){
    it('single item returns 1 item', function(){
      var context = [
        { sessionID: '6c3c9f61-8f22-4e4c-8619-2eb0282b14df',
            uuid: 'f46b177e-4add-4a27-993c-de69f2ef9b2d',
            timestamp: '2014-01-10T06:44:52.509Z',
            data: { type: 'colour', value: 'pink', method: 'exact' },
            _id: '52cf96e4e9d40c0000d64696' }
      ];
      var target = session.newestUnique(context); 
      assert.equal(target.length, 1);
      assert.equal();
      
    });
    it('multple single item returns multiple item', function(){
      var context = [
        { sessionID: '6c3c9f61-8f22-4e4c-8619-2eb0282b14df',
            uuid: 'f46b177e-4add-4a27-993c-de69f2ef9b2d',
            timestamp: '2014-01-10T06:44:52.509Z',
            data: { type: 'colour', value: 'pink', method: 'exact' },
            _id: '52cf96e4e9d40c0000d64696' },
        { sessionID: '6c3c9f61-8f22-4e4c-8619-2eb0282b14df',
            uuid: 'f46b177e-4add-4a27-993c-de69f2ef9b2d',
            timestamp: '2014-01-10T06:44:54.509Z',
            data: { type: 'colour', value: 'blue', method: 'exact' },
            _id: '52cf96e4e9d40c0000d64696' },
        { sessionID: '6c3c9f61-8f22-4e4c-8619-2eb0282b14df',
            uuid: 'f46b177e-4add-4a27-993c-de69f2ef9b2d',
            timestamp: '2014-01-10T06:44:33.509Z',
            data: { type: 'style', value: 'pumps', method: 'exact' },
            _id: '52cf96e4e9d40c0000d64696' }
      ];
      var target = session.newestUnique(context); 
      assert.equal(target.length, 3);
      assert.equal();
      
    });
    it('duplicate as single item return single newest item', function(){
      var context = [
        { sessionID: '6c3c9f61-8f22-4e4c-8619-2eb0282b14df',
            uuid: 'f46b177e-4add-4a27-993c-de69f2ef9b2d',
            timestamp: '2014-01-10T06:44:52.509Z',
            data: { type: 'colour', value: 'pink', method: 'exact' },
            _id: '52cf96e4e9d40c0000d64696' },
        { sessionID: '6c3c9f61-8f22-4e4c-8619-2eb0282b14df',
            uuid: 'f46b177e-4add-4a27-993c-de69f2ef9b2d',
            timestamp: '2014-01-10T06:50:52.509Z',
            data: { type: 'colour', value: 'pink', method: 'exact' },
            _id: '52cf96e4e9d40c0000d62796' },
        { sessionID: '6c3c9f61-8f22-4e4c-8619-2eb0282b14df',
            uuid: 'f46b177e-4add-4a27-993c-de69f2ef9b2d',
            timestamp: '2014-01-10T06:46:52.509Z',
            data: { type: 'colour', value: 'pink', method: 'exact' },
            _id: '52cf96e4e9d40c0000d62796' }
      ];
      var target = session.newestUnique(context); 
      assert.equal(target.length, 1);
      assert.equal(target[0].timestamp, '2014-01-10T06:50:52.509Z');
      
    });
    it('multiple of some of which are duplicate single item return multiple single newest item', function(){
      var context = [
        { sessionID: '6c3c9f61-8f22-4e4c-8619-2eb0282b14df',
            uuid: 'f46b177e-4add-4a27-993c-de69f2ef9b2d',
            timestamp: '2014-01-10T06:44:52.509Z',
            data: { type: 'colour', value: 'pink', method: 'exact' },
            _id: '52cf96e4e9d40c0000d64696' },
        { sessionID: '6c3c9f61-8f22-4e4c-8619-2eb0282b14df',
            uuid: 'f46b177e-4add-4a27-993c-de69f2ef9b2d',
            timestamp: '2014-01-10T06:46:52.509Z',
            data: { type: 'colour', value: 'pink', method: 'exact' },
            _id: '52cf96e4e9d40c0000d62796' },
        { sessionID: '6c3c9f61-8f22-4e4c-8619-2eb0282b14df',
            uuid: 'f46b177e-4add-4a27-993c-de69f2ef9b2d',
            timestamp: '2014-01-10T06:44:54.509Z',
            data: { type: 'colour', value: 'blue', method: 'exact' },
            _id: '52cf96e4e9d40c0000d64696' },
        { sessionID: '6c3c9f61-8f22-4e4c-8619-2eb0282b14df',
            uuid: 'f46b177e-4add-4a27-993c-de69f2ef9b2d',
            timestamp: '2014-01-10T06:44:23.509Z',
            data: { type: 'style', value: 'pumps', method: 'exact' },
            _id: '52cf96e4e9d40c0000d64696' },
        { sessionID: '6c3c9f61-8f22-4e4c-8619-2eb0282b14df',
            uuid: 'f46b177e-4add-4a27-993c-de69f2ef9b2d',
            timestamp: '2014-01-10T06:50:12.509Z',
            data: { type: 'colour', value: 'pink', method: 'exact' },
            _id: '52cf96e4e9d40c0000d62796' },
        { sessionID: '6c3c9f61-8f22-4e4c-8619-2eb0282b14df',
            uuid: 'f46b177e-4add-4a27-993c-de69f2ef9b2d',
            timestamp: '2014-01-10T06:44:33.509Z',
            data: { type: 'style', value: 'pumps', method: 'exact' },
            _id: '52cf96e4e9d40c0000d64696' }
      ];
      var target = session.newestUnique(context); 
      assert.equal(target.length, 3);
      assert.equal(target[0].timestamp, '2014-01-10T06:50:12.509Z');
      assert.equal(target[0].data.type, 'colour');
      assert.equal(target[0].data.value, 'pink');
      assert.equal(target[1].timestamp, '2014-01-10T06:44:54.509Z');
      assert.equal(target[1].data.type, 'colour');
      assert.equal(target[1].data.value, 'blue');
      assert.equal(target[2].timestamp, '2014-01-10T06:44:33.509Z');
      assert.equal(target[2].data.type, 'style');
      assert.equal(target[2].data.value, 'pumps');
      
    });
  });
  describe('processItems', function(){
    it('empty context empty response', function(){
      var context = [ ];
      var target = session.processItems(context); 
      assert.equal(target.length, 0);
    });
    it('single item has correct ageScore', function(){
      var context = [
        { sessionID: '6c3c9f61-8f22-4e4c-8619-2eb0282b14df',
            uuid: 'f46b177e-4add-4a27-993c-de69f2ef9b2d',
            timestamp: '2014-01-10T06:44:52.509Z',
            data: { type: 'colour', value: 'pink', method: 'exact' },
            _id: '52cf96e4e9d40c0000d64696' }
      ];
      var target = session.processItems(context); 
      assert.equal(target.length, 1);
      assert.equal(target[0].ageScore, 0.5);
      
    });
    
  })
})
  
describe('session', function(){
  describe('processItems', function(){
    it('should return -1 when the value is not present', function(){
      var context = [ { sessionID: '6c3c9f61-8f22-4e4c-8619-2eb0282b14df',
          uuid: 'f46b177e-4add-4a27-993c-de69f2ef9b2d',
          timestamp: '2014-01-10T06:44:52.509Z',
          data: { type: 'colour', value: 'pink', method: 'exact' },
          _id: '52cf96e4e9d40c0000d64696' },
        { sessionID: '6c3c9f61-8f22-4e4c-8619-2eb0282b14df',
          uuid: 'f46b177e-4add-4a27-993c-de69f2ef9b2d',
          timestamp: '2014-01-10T06:44:52.509Z',
          data: { type: 'colour', value: 'blue', method: 'exact' },
          _id: '52cf96e4e9d40c0000d64697' },
        { sessionID: '6c3c9f61-8f22-4e4c-8619-2eb0282b14df',
          uuid: 'f46b177e-4add-4a27-993c-de69f2ef9b2d',
          timestamp: '2014-01-10T06:44:52.509Z',
          data: { type: 'style', value: 'pumps', method: 'exact' },
          _id: '52cf96e4e9d40c0000d64698' },
        { sessionID: '6c3c9f61-8f22-4e4c-8619-2eb0282b14df',
          uuid: 'f46b177e-4add-4a27-993c-de69f2ef9b2d',
          timestamp: '2014-01-10T06:46:22.317Z',
          data: { type: 'colour', value: 'black', method: 'exact' },
          _id: '52cf973ee9d40c0000d64699' },
        { sessionID: '6c3c9f61-8f22-4e4c-8619-2eb0282b14df',
          uuid: 'f46b177e-4add-4a27-993c-de69f2ef9b2d',
          timestamp: '2014-01-10T06:46:22.317Z',
          data: { type: 'colour', value: 'blue', method: 'exact' },
          _id: '52cf973ee9d40c0000d6469a' },
        { sessionID: '6c3c9f61-8f22-4e4c-8619-2eb0282b14df',
          uuid: 'f46b177e-4add-4a27-993c-de69f2ef9b2d',
          timestamp: '2014-01-10T06:46:22.317Z',
          data: { type: 'colour', value: 'green', method: 'exact' },
          _id: '52cf973ee9d40c0000d6469b' },
        { sessionID: '6c3c9f61-8f22-4e4c-8619-2eb0282b14df',
          uuid: 'f46b177e-4add-4a27-993c-de69f2ef9b2d',
          timestamp: '2014-01-10T07:26:05.798Z',
          data: { type: 'colour', value: 'blue', method: 'exact' },
          _id: '52cfa08de9d40c0000d6469c' },
        { sessionID: '6c3c9f61-8f22-4e4c-8619-2eb0282b14df',
          uuid: 'f46b177e-4add-4a27-993c-de69f2ef9b2d',
          timestamp: '2014-01-10T07:33:45.569Z',
          data: { type: 'colour', value: 'green', method: 'exact' },
          _id: '52cfa259e9d40c0000d6469d' },
        { sessionID: '6c3c9f61-8f22-4e4c-8619-2eb0282b14df',
          uuid: 'f46b177e-4add-4a27-993c-de69f2ef9b2d',
          timestamp: '2014-01-10T07:34:27.092Z',
          data: { type: 'colour', value: 'blue', method: 'exact' },
          _id: '52cfa283e9d40c0000d6469e' },
        { sessionID: '6c3c9f61-8f22-4e4c-8619-2eb0282b14df',
          uuid: 'f46b177e-4add-4a27-993c-de69f2ef9b2d',
          timestamp: '2014-01-10T07:34:48.479Z',
          data: { type: 'colour', value: 'yellow', method: 'exact' },
          _id: '52cfa298e9d40c0000d6469f' } ];
          
          
          // processItems
      assert.equal(-1, [1,2,3].indexOf(5));
      assert.equal(-1, [1,2,3].indexOf(0));
    })
  })
})