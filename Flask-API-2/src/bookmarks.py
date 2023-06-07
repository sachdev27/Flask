from flask import Blueprint,request,jsonify
import validators
from src.constants.http_status_codes import *
from flask_jwt_extended import get_jwt_identity,jwt_required
from src.database import Bookmark,db




bookmarks = Blueprint("bookmarks",__name__,url_prefix="/api/v1/bookmarks")


@bookmarks.route('/',methods=['POST','GET'])
@jwt_required()
def handle_bookmark():
    current_user = get_jwt_identity()
    
    if request.method == 'POST':
        
        body = request.get_json().get('body','')
        url = request.get_json().get('url','')
        
        if not validators.url(url): # Validate URL
            return jsonify({
                'error' : 'Invalid URL'
            }),HTTP_400_BAD_REQUEST
        
        if Bookmark.query.filter_by(url=url).first():
            return jsonify({
                'error': 'URL already exist'
            }), HTTP_409_CONFLICT
            
        bookmark_obj = Bookmark(url=url,body=body,user_id=current_user)
        
        db.session.add(bookmark_obj)
        db.session.commit()
        
        
        return jsonify({
            'id' : bookmark_obj.id,
            'url' : bookmark_obj.url,
            'short_url' : bookmark_obj.short_url,
            'visits' : bookmark_obj.visits,
            'body' : bookmark_obj.body,
            'created_at' : bookmark_obj.create_at,
            'updated_at' : bookmark_obj.updated_at
        }),HTTP_201_CREATED
        
    else:
        page = request.args.get('page',1,type=int)
        per_page = request.args.get('per_page',5,type=int)
        
        bookmarks =  Bookmark.query.filter_by(user_id=current_user).paginate(
            page=page,per_page=per_page
            ) #Pagination 
            # Definition : Pagination is the process of dividing a document into discrete pages,
            # here we are dividing the data into discrete pages.
            #   /?page=2   ->  2nd page
            #   /?page=2/per_page=10  -> 2nd page with 10 bookmarks per page
        
        data = []
        
        for bookmark in bookmarks:
            data.append({
                'id' : bookmark.id,
                'url' : bookmark.url,
                'short_url' : bookmark.short_url,
                'visits' : bookmark.visits,
                'body' : bookmark.body,
                'created_at' : bookmark.create_at,
                'updated_at' : bookmark.updated_at
            })
        
        """Meta data
        
        page : current page
        pages : total pages
        total_count : total bookmarks
        prev_page : previous page
        next_page : next page
        has_next : has next page
        has_prev : has previous page
        """
        
        meta={
            "page":bookmarks.page,
            "pages":bookmarks.pages,
            'total_count': bookmarks.total,
            'prev_page' : bookmarks.prev_num,
            'next_page' : bookmarks.next_num,
            'has_next' : bookmarks.has_next,
            'hast_prev' : bookmarks.has_prev,
        }
        
        
        return jsonify({
            'data' : data,
            'meta' : meta
            }),HTTP_200_OK

# ------------------------------------------------------------------------------------------


@bookmarks.get("/<int:id>")
@jwt_required()
def get_bookmark(id):
    current_user = get_jwt_identity()
    
    bookmark = Bookmark.query.filter_by(id=id,user_id=current_user).first()
    
    if bookmark:
        return jsonify({
            'id' : bookmark.id,
            'url' : bookmark.url,
            'short_url' : bookmark.short_url,
            'visits' : bookmark.visits,
            'body' : bookmark.body,
            'created_at' : bookmark.create_at,
            'updated_at' : bookmark.updated_at
        }),HTTP_200_OK
    else:
        return jsonify({
            'message' : 'No bookmarks exits'
        }),HTTP_404_NOT_FOUND
        
        
# ------------------------------------------------------------------------------------------
        
@bookmarks.put('/<int:id>')
@bookmarks.patch('/<int:id>')
@jwt_required()

def update(id):
    
    current_user = get_jwt_identity()
    bookmark = Bookmark.query.filter_by(id=id,user_id=current_user).first() # Get the unique bookmark
    
    if  not bookmark:
        return jsonify({
            "Message" : "No Bookmark exist with this ID"
        })
                
    else:
        new_url = request.get_json().get('url','')
        new_body = request.get_json().get('body','')
        
        if not validators.url(new_url):
            return jsonify({
            "Message" : 'Not Valid Url'
        })
            
        bookmark.url = new_url
        bookmark.body = new_body
        
        db.session.commit()
        
        return jsonify({
            'id' : bookmark.id,
            'url' : bookmark.url,
            'short_url' : bookmark.short_url,
            'visits' : bookmark.visits,
            'body' : bookmark.body,
            'created_at' : bookmark.create_at,
            'updated_at' : bookmark.updated_at
        }),HTTP_200_OK

# ------------------------------------------------------------------------------------------

     
@bookmarks.delete("/<int:id>")
@jwt_required()
def delete_bookmark(id):
    current_user = get_jwt_identity()
    
    bookmark = Bookmark.query.filter_by(id=id,user_id=current_user).first()
    
    if bookmark:
        db.session.delete(bookmark)
        db.session.commit()
        
        return jsonify({
            'Message' : "Bookmark was deleted"
        }),HTTP_204_NO_CONTENT
    else:
        return jsonify({
            'message' : 'No bookmarks exits'
        }),HTTP_404_NOT_FOUND
    