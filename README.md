# MLOps 수업 실습자료

## 실험 준비

1. Clone or update the public lab materials
    - If cloning for the first time:
    ```bash
    cd ~/
    git clone https://github.com/Integrative-Data-Comprehension-Lab/Class_MLOps_Lab_public
    ```
    - If you already cloned before:
    ```bash
    cd ~/Class_MLOps_Lab_public
    git pull
    ```

2. cloning your private repository
```bash
cd ~/
git clone https://YOUR_USERNAME:YOUR_TOKEN@github.com/\
YOUR_USERNAME/YOUR_PRIVATE_REPOSITORY_NAME.git
```

3. 실습 자료를 개인 레포지토리로 가져오기
```bash
cd ~/
cp Class_MLOps_Lab_public/README.md YOUR_PRIVATE_REPOSITORY_NAME/
cp -r Class_MLOps_Lab_public/lab_XX YOUR_PRIVATE_REPOSITORY_NAME/
```

4. 실습 진행 전 상태를 푸쉬하기
```bash
cd ~/YOUR_PRIVATE_REPOSITORY_NAME
git status

git add lab_XX
git status

git commit -m "before lab_XX"
git push

git log --oneline
```
