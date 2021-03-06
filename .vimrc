"" General configurations 
" Use UTF-8 without BOM
set encoding=utf-8 nobomb
" Add the g flag to search/replace by default
set gdefault
" convert tabs to 4 spaces
set expandtab
set shiftwidth=4
set tabstop=4

" vundle configuration

set nocompatible              
filetype off                  

" set the runtime path to include Vundle and initialize
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()

Plugin 'gmarik/Vundle.vim'
Plugin 'scrooloose/nerdtree'


" All of your Plugins must be added before the following line
call vundle#end()            
filetype plugin indent on    

" nerdtree
autocmd StdinReadPre * let s:std_in=1
autocmd VimEnter * if argc() == 0 && !exists("s:std_in") | NERDTree | endif
map <C-n> :NERDTreeToggle<CR>
